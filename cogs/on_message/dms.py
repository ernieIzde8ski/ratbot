from asyncio import sleep
from typing import Union

import discord
from discord.ext import commands


class DM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.latest = None
        self.latest_task = None

    @commands.Cog.listener("on_message")
    async def log_message(self, msg):
        # pass only if in direct messages
        if msg.guild: return
        # log own messages as an embed in the proper channel
        if msg.author == self.bot.user:
            embed = discord.Embed(title=f"Direct Message → {msg.channel.recipient} ({msg.channel.recipient.id})",
                                  description=msg.content, timestamp=msg.created_at, color=discord.Color.orange())
            return await self.bot.config.channels.log.send(embed=embed)
        # log message only if is not bot user
        elif msg.author.bot:
            return
        else:
            embed = discord.Embed(title=f"Direct Message — {msg.author} ({msg.author.id})",
                                  description=msg.content, timestamp=msg.created_at, color=discord.Color.dark_blue())

            await self.bot.config.channels.log.send(embed=embed)
            # also save for later
            if self.latest_task:
                self.latest_task.cancel()
            self.latest_task = self.bot.loop.create_task(self.latest_message(msg))

    async def latest_message(self, msg):
        self.latest = msg
        await sleep((60 * 5))
        self.latest = None

    @commands.Cog.listener("on_message")
    async def respond_to_message(self, msg):
        if not self.latest or msg.channel != self.bot.config.channels.log:
            return
        if msg.author.bot:
            return
        if msg.content.startswith("r."):
            return
        await self.latest.channel.send(f"[{msg.author}] {msg.content}")
        await msg.delete()

    @commands.command(aliases=["vessel", "wessel"])
    @commands.is_owner()
    async def echo(self, ctx, messageable: Union[commands.TextChannelConverter, commands.UserConverter, int, None], *,
                   text: str):
        """Bogstandard echo command"""
        if not messageable:
            messageable = ctx.channel
        await messageable.send(text)

    @commands.command(aliases=["r"])
    @commands.is_owner()
    async def reply(self, ctx, *, text: str):
        if not self.latest:
            await ctx.channel.send("There's no Latest Mesage Bro...................")
        else:
            await self.latest.channel.send(text)
            await ctx.message.delete()


def setup(bot):
    bot.add_cog(DM(bot))
