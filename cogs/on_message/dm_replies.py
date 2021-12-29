import re
from asyncio import sleep
from os import remove
from typing import Optional, Union

import discord
from aiohttp.client import ClientSession
from discord.ext import commands
from utils.classes import RatBot
from utils.functions import safe_load


class Replies(commands.Cog):
    def __init__(self, bot: RatBot):
        self.bot = bot
        self.allowed_mentions = discord.AllowedMentions.all()
        self.task = None

    async def _update_message(self, message: discord.Message) -> None:
        self.bot.data.msg = message
        await sleep(600)
        self.bot.data.msg = None

    async def update_message(self, message: discord.Message) -> None:
        if self.task:
            self.task.cancel()
        self.task = self.bot.loop.create_task(self._update_message(message))

    @commands.command()
    @commands.check(lambda ctx: ctx.channel == ctx.bot.c.DMs or (isinstance(ctx.channel, discord.DMChannel) and ctx.channel == ctx.bot._message.channel))
    async def clear(self, ctx: commands.Context):
        """Clear the DM channel"""
        if not self.task or not self.bot.data.msg:
            raise commands.CommandError("No DM channel is currently open")
        else:
            await ctx.send(f"Clearing open channel with {self.bot.data.msg.channel.recipient}")
            await sleep(0.5)
            self.task.cancel()
            self.bot.data.msg = None

    @commands.command()
    @commands.check(lambda ctx: ctx.channel == ctx.bot.c.DMs or ctx.author.id == ctx.bot.owner_id)
    async def block(self, ctx: commands.Context, *, blockee: Optional[discord.User]):
        """Block a discord.User"""
        if blockee:
            await ctx.send(f"Blocked {blockee}")
            self.bot.block_check.update_blocked(blockee)
            if self.task and self.bot.data.msg and blockee == self.bot.data.msg:
                self.task.cancel()
                self.bot.data.msg = None
        elif self.bot.data.msg:
            await ctx.send(f"Blocked {self.bot.data.msg.author}")
            self.bot.block_check.update_blocked(self.bot.data.msg.author)
            if self.task:
                self.task.cancel()
                self.bot.data.msg = None
        else:
            raise commands.MissingRequiredArgument("blockee is a required argument that is missing.")

    @commands.command()
    @commands.check(lambda ctx: ctx.channel == ctx.bot.c.DMs or ctx.author.id == ctx.bot.owner_id)
    async def unblock(self, ctx: commands.Context, *, blockee: Union[discord.Member, discord.User]):
        if blockee.id not in self.bot.block_check.blocked:
            raise commands.BadArgument("blockee {blockee} is not blocked")
        else:
            self.bot.block_check.unblock(blockee)
            await ctx.send(f"Unblocked {blockee}")

    @commands.command()
    @commands.is_owner()
    async def refresh_blocked(self, ctx: commands.Context):
        self.bot.block_check.set_blocked(safe_load("data/blocked.json", []))
        await ctx.send("Refreshed block list")

    @commands.Cog.listener()
    async def on_private_message(self, message: discord.Message):
        await self.update_message(message)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot or message.author.id in self.bot.block_check.blocked:
            return
        elif not self.bot.data.msg or message.channel != self.bot.status_channels.DM:
            return
        elif re.match(r"^.*\s*clear.*$", message.content):
            return

        [resp, files, failed_files] = await self.get_resp(message)
        try:
            await self.bot.data.msg.channel.send(resp, files=files, allowed_mentions=self.allowed_mentions)
        except discord.Forbidden:
            await message.reply(f"Error: Cannot send messages to {self.bot.data.msg.author}, closing the channel")
            if self.task:
                self.task.cancel()
            self.bot.data.msg = None
        except discord.HTTPException as e:
            await message.reply(f"{e.__class__.__name__}: {e}")
        else:
            if not failed_files:
                await message.delete()

        for file in map(lambda f: f.fp.name, files):
            remove(file)

    async def get_resp(self, message: discord.Message) -> list:
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
                        file = discord.File(await self.download_attachment(session, attachment))
                        files.append(file)
        if failed_files:
            resp += f"\n*{failed_files} attachment(s) failed to send.*"
        return [resp, files, failed_files]

    @staticmethod
    async def download_attachment(session: ClientSession, attachment: discord.Attachment) -> str:
        path = f"data/temporary/{attachment.filename}"
        resp = await session.get(attachment.url)
        resp = await resp.read()
        with open(path, "wb+") as file:
            file.write(resp)
        return path


def setup(bot: RatBot):
    bot.add_cog(Replies(bot))
