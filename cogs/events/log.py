from typing import Literal

from discord import Color, Embed
from discord.ext import commands
from utils import RatBot, RatCog


class Log(RatCog):
    """Online/offline status logging"""

    # TODO: Rewrite as cogs.power

    async def _on_ready(self):
        self.bot.status_channels.get_channels(self.bot)

    def embed_constructor(self, status: Literal["online", "offline"]):
        if status == "online":
            return Embed(title=f"{self.emojis.power_on} Online!", color=Color.dark_green())
        else:
            return Embed(title=f"{self.emojis.power_off} Offline!", color=Color.from_rgb(91, 10, 0))

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user.name}#{self.bot.user.discriminator} online!")
        await self.bot.status_channels.Status.send(embed=self.embed_constructor("online"))

    @commands.command()
    @commands.is_owner()
    async def die(self, ctx: commands.Context):
        """Shuts down bot"""
        await ctx.message.add_reaction("☑️")
        await self.bot.status_channels.Status.send(embed=self.embed_constructor("offline"))
        await self.bot.close()


setup = Log.basic_setup
