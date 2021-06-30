from typing import Optional
from aiohttp.client import ClientSession
from discord.ext import commands
from discord import Message, Attachment, File, AllowedMentions, User
from discord import Forbidden, HTTPException
from asyncio import sleep
from modules._json import safe_load
from os import remove
import re


class Replies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_mentions = AllowedMentions.all()
        self.message = None
        self.task = None

    async def _update_message(self, message: Message) -> None:
        self.message = message
        await sleep(600)
        self.message = None

    async def update_message(self, message: Message) -> None:
        if self.task:
            self.task.cancel()
        self.task = self.bot.loop.create_task(self._update_message(message))

    @commands.command()
    @commands.check(lambda ctx: ctx.channel == ctx.bot.c.DMs)
    async def clear(self, ctx):
        """Clear the DM channel"""
        if not self.task:
            await ctx.send("There's nothing to clear!")
        else:
            await ctx.send(f"Clearing open channel with {self.message.author}")
            self.task.cancel()
            self.message = None

    @commands.command()
    @commands.check(lambda ctx: ctx.channel == ctx.bot.c.DMs or ctx.author.id == ctx.bot.owner_id)
    async def block(self, ctx, *, blockee: Optional[User]):
        """Block a discord.User"""
        print(ctx.author.id, ctx.bot.owner_id)
        if not blockee and not self.message:
            await ctx.send("There's no one to block!")
        elif not blockee:
            await ctx.send(f"Blocked {self.message.author}")
            self.bot._check.update_blocked(self.message.author)
            if self.task:
                self.task.cancel()
                self.message = None
        else:
            await ctx.send(f"Blocked {blockee}")
            self.bot._check.update_blocked(blockee)
            if self.message:
                if blockee == self.message.author:
                    self.task.cancel()
                    self.message = None

    @commands.command()
    @commands.check(lambda ctx: ctx.channel == ctx.bot.c.DMs or ctx.author.id == ctx.bot.owner_id)
    async def unblock(self, ctx, *, blockee: Optional[User]):
        if not blockee:
            return await ctx.send("There's no one to unblock!")
        elif blockee.id not in self.bot._check.blocked:
            print(self.bot._check.blocked)
            return await ctx.send(f"{blockee} is not blocked!")
        else:
            self.bot._check.unblock(blockee)
            return await ctx.send(f"Unblocked {blockee}")

    @commands.command()
    @commands.is_owner()
    async def refresh_blocked(self, ctx):
        self.bot._check.set_blocked(safe_load("data/blocked.json", []))
        await ctx.send("Refreshed block list")

    @commands.Cog.listener()
    async def on_private_message(self, message: Message):
        if re.match(r"^.*?\s*clear$", message.content):
            return
        await self.update_message(message)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot or message.author.id in self.bot._check.blocked:
            return
        elif not self.message or message.channel != self.bot.c.DMs:
            return
        elif re.match(r"^.*?\s*clear$", message.content):
            return
        
        [resp, files, failed_files] = await self.get_resp(message)
        try:
            await self.message.channel.send(resp, files=files, allowed_mentions=self.allowed_mentions)
        except Forbidden:
            await message.reply(f"Error: Cannot send messages to {self.message.author}")
            if self.task:
                self.task.cancel()
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
