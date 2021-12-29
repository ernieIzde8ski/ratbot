from discord import Color, Embed
from discord.ext import commands
from utils.functions import safe_load
from utils.classes import RatBot


class Log(commands.Cog):
    def __init__(self, bot: RatBot):
        self.bot = bot
        self.emoji = safe_load("data/emoji.json", ["🐣", "🎃"])

    def get_channels(self):
        if not self.bot.status_channels.loaded:
            self.bot.status_channels.get_channels(self.bot)

    def embed_constructor(self, status: str):
        if status == "online":
            return Embed(title=f"{self.emoji[0]} Online!", color=Color.dark_green())
        elif status == "offline":
            return Embed(title=f"{self.emoji[1]} Offline!", color=Color.from_rgb(91, 10, 0))

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
