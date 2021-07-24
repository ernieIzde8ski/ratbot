import re
from aiohttp.client import ClientSession
from asyncio import sleep
from discord import Forbidden, HTTPException, Message, Attachment, File, AllowedMentions, User
from discord.ext import commands
from os import remove
from typing import Optional, Union

from discord.member import Member
from discord import DMChannel

from modules._json import safe_load


class Replies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_mentions = AllowedMentions.all()
        self.bot._message = None
        self.task = None

    async def _update_message(self, message: Message) -> None:
        self.bot._message = message
        await sleep(600)
        self.bot._message = None

    async def update_message(self, message: Message) -> None:
        if self.task:
            self.task.cancel()
        self.task = self.bot.loop.create_task(self._update_message(message))

    @commands.command()
    @commands.check(lambda ctx: ctx.channel == ctx.bot.c.DMs or (isinstance(ctx.channel, DMChannel) and ctx.channel == ctx.bot._message.channel))
    async def clear(self, ctx):
        """Clear the DM channel"""
        if not self.task:
            raise commands.CommandError("No DM channel is currently open")
        else:
            await ctx.send(f"Clearing open channel with {self.bot._message.channel.recipient}")
            await sleep(0.5)
            self.task.cancel()
            self.bot._message = None

    @commands.command()
    @commands.check(lambda ctx: ctx.channel == ctx.bot.c.DMs or ctx.author.id == ctx.bot.owner_id)
    async def block(self, ctx, *, blockee: Optional[User]):
        """Block a discord.User"""
        if not blockee and not self.bot._message:
            raise commands.MissingRequiredArgument("blockee is a required argument that is missing.")
        elif not blockee:
            await ctx.send(f"Blocked {self.bot._message.author}")
            self.bot._check.update_blocked(self.bot._message.author)
            if self.task:
                self.task.cancel()
                self.bot._message = None
        else:
            await ctx.send(f"Blocked {blockee}")
            self.bot._check.update_blocked(blockee)
            if self.bot._message:
                if blockee == self.bot._message.author:
                    self.task.cancel()
                    self.bot._message = None

    @commands.command()
    @commands.check(lambda ctx: ctx.channel == ctx.bot.c.DMs or ctx.author.id == ctx.bot.owner_id)
    async def unblock(self, ctx, *, blockee: Union[Member, User]):
        if blockee.id not in self.bot._check.blocked:
            raise commands.BadArgument("blockee {blockee} is not blocked")
        else:
            self.bot._check.unblock(blockee)
            await ctx.send(f"Unblocked {blockee}")

    @commands.command()
    @commands.is_owner()
    async def refresh_blocked(self, ctx):
        self.bot._check.set_blocked(safe_load("data/blocked.json", []))
        await ctx.send("Refreshed block list")

    @commands.Cog.listener()
    async def on_private_message(self, message: Message):
        await self.update_message(message)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot or message.author.id in self.bot._check.blocked:
            return
        elif not self.bot._message or message.channel != self.bot.c.DMs:
            return
        elif re.match(r"^.*\s*clear.*$", message.content):
            return

        [resp, files, failed_files] = await self.get_resp(message)
        try:
            await self.bot._message.channel.send(resp, files=files, allowed_mentions=self.allowed_mentions)
        except Forbidden:
            await message.reply(f"Error: Cannot send messages to {self.bot._message.author}, closing the channel")
            if self.task:
                self.task.cancel()
            self.bot._message = None
        except HTTPException as e:
            await message.reply(f"{e.__class__.__name__}: {e}")
        else:
            if not failed_files:
                await message.delete()

        for file in map(lambda f: f.fp.name, files):
            remove(file)

    async def get_resp(self, message: Message) -> list:
        resp = f"[{message.author}] {message.content}"
        files = []
        failed_files = 0
        if message.attachments:
            async with ClientSession() as session:
                for attachment in message.attachments:
                    if attachment.size > 4000000:
                        failed_files += 1
                        continue
                    else:
                        file = File(await self.download_attachment(session, attachment))
                        files.append(file)
        if failed_files:
            resp += f"\n*{failed_files} attachment(s) failed to send.*"
        return [resp, files, failed_files]

    @staticmethod
    async def download_attachment(session: ClientSession, attachment: Attachment) -> str:
        path = f"data/temporary/{attachment.filename}"
        resp = await session.get(attachment.url)
        resp = await resp.read()
        with open(path, "wb+") as file:
            file.write(resp)
        return path


def setup(bot):
    bot.add_cog(Replies(bot))
