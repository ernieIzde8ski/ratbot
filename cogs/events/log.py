from typing import Literal
from discord import Color, Embed
from discord.ext import commands
from utils.functions import safe_load
from utils.classes import RatBot


class Log(commands.Cog):
    def __init__(self, bot: RatBot):
        self.bot = bot
        self.wakeup, self.close = safe_load("data/emoji.json", ["🐣", "🎃"])

    def get_channels(self):
        if not self.bot.status_channels.loaded:
            self.bot.status_channels.get_channels(self.bot)

    def embed_constructor(self, status: Literal["online"] | Literal["offline"]):
        if status == "online":
            return Embed(title=f"{self.wakeup} Online!", color=Color.dark_green())
        else:
            return Embed(title=f"{self.close} Offline!", color=Color.from_rgb(91, 10, 0))

    @commands.Cog.listener()
    async def on_ready(self):
        self.get_channels()
        print(f"{self.bot.user.name}#{self.bot.user.discriminator} online!")
        await self.bot.status_channels.Status.send(embed=self.embed_constructor("online"))

    @commands.command()
    @commands.is_owner()
    async def die(self, ctx: commands.Context):
        """Shuts down bot"""
        self.get_channels()
        await ctx.message.add_reaction("☑️")
        await self.bot.status_channels.Status.send(embed=self.embed_constructor("offline"))
        await self.bot.close()


def setup(bot: RatBot):
    cog = Log(bot)
    if bot.user:
        cog.get_channels()
    bot.add_cog(cog)
