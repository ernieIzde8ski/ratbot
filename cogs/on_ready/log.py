from discord.ext import commands
from discord import Embed, Color
from discord.user import ClientUser
from modules.json import safe_load


class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = safe_load("data/emoji.json", ["🐣", "🎃"])

    def get_channels(self):
        if not self.bot.cs.loaded:
            self.bot.cs.get_channels(self.bot)

    def embed_constructor(self, status: str):
        if status == "online":
            return Embed(title=f"{self.emoji[0]} Online!", color=Color.dark_green())
        elif status == "offline":
            return Embed(title=f"{self.emoji[1]} Offline!", color=Color.from_rgb(91, 10, 0))

    @commands.Cog.listener()
    async def on_ready(self):
        self.get_channels()
        print(f"{self.bot.user.name}#{self.bot.user.discriminator} online!")
        await self.bot.cs.k["Status"].send(embed = self.embed_constructor("online"))
    
    @commands.command()
    async def die(self, ctx):
        self.get_channels()
        await self.bot.cs.k["Status"].send(embed = self.embed_constructor("offline"))
        await self.bot.close()


def setup(bot):
    cog = Log(bot)
    if bot.user:
        cog.get_channels()
    bot.add_cog(cog)
