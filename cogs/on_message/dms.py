import json
from asyncio import sleep
from typing import Union, Optional

import discord.ext.commands as commands
from discord import Color, Embed, User


async def is_log_channel(ctx) -> bool:  # check for log channel
    return ctx.channel.id == 715297562613121084


class DM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.latest = None
        self.latest_task = None
        with open("configs/blocked.json", "r") as f:
            self.blocked_list = json.load(f)

    @commands.Cog.listener("on_message")
    async def log_message(self, msg):
        # pass only if in direct messages
        if msg.guild: return
        if msg.author.id in self.blocked_list["ids"]: return
        # log own messages as an embed in the proper channel
        if msg.author == self.bot.user:
            embed = Embed(title=f"Direct Message → {msg.channel.recipient} ({msg.channel.recipient.id})",
                          description=msg.content, color=Color.orange())
            return await self.bot.config.channels.log.send(embed=embed)
        # log message only if is not bot user
        elif msg.author.bot:
            return
        else:
            embed = Embed(title=f"Direct Message — {msg.author} ({msg.author.id})",
                          description=msg.content, color=Color.dark_blue())
            if msg.attachments:
                embed.set_image(url=msg.attachments[0].url)
                if len(msg.attachments) > 1:
                    embed.set_footer(text=f"{len(msg.attachments) - 1} attachment(s) not shown")
                else:
                    embed.set_footer(text="1 attachment")
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
        if msg.channel != self.bot.config.channels.log or not self.latest:
            return
        if msg.author.bot or msg.content.startswith(tuple(self.bot.config.prefix)):
            return
        await self.latest.channel.send(f"[{msg.author}] {msg.content}")
        await msg.delete()

    @commands.command(aliases=["vessel", "wessel"])
    @commands.is_owner()
    async def echo(self, ctx, messageable: Union[commands.TextChannelConverter, commands.UserConverter, None], *,
                   text: str):
        """Bogstandard echo command"""
        if not messageable:
            messageable = ctx.channel
        await messageable.send(text)

    @commands.command(aliases=["r"])
    @commands.is_owner()
    async def reply(self, ctx, *, text: str):
        """Replies to the latest direct message from within 5 minutes"""
        if self.latest:
            await self.latest.channel.send(text)
            await ctx.message.delete()
        else:
            await ctx.channel.send("There's no Latest Mesage Bro...................")

    @commands.command(aliases=["clear"])
    @commands.check(is_log_channel)
    async def clear_latest(self, ctx):
        """Clears the latest message from replying"""
        if self.latest:
            self.latest_task.cancel()
            self.latest = None
            await ctx.channel.send("Delted")
        else:
            await ctx.channel.send("There Dont Be Anything To Clear Doe .")

    @commands.command(aliases=["b", "block"])
    @commands.check(is_log_channel)
    @commands.is_owner()
    async def block_recipient(self, ctx, blockee: Optional[User]):
        if not blockee and not self.latest:
            return await ctx.channel.send("You aint given me no input")
        elif not blockee:
            blockee = self.latest.author

        if blockee.id in self.blocked_list["ids"]:
            await ctx.channel.send("User already blocked")
        else:
            self.blocked_list["ids"].append(blockee.id)
            with open("configs/blocked.json", "w") as f:
                json.dump(self.blocked_list, f, indent=2)
            if self.latest:
                self.latest_task.cancel()
                self.latest = None
            await blockee.send("Blocked")


def setup(bot):
    bot.add_cog(DM(bot))
