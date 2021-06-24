from discord.ext import commands
from discord import Embed, Color
from discord.user import ClientUser
from modules.json import safe_load


class Log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = safe_load("data/emoji.json", "🎃")

    def get_channels(self):
        if not self.bot.channels.loaded:
            self.bot.channels.get_channels(self.bot)

    def embed_constructor(self):
        return Embed(title=f"{self.emoji} Online!", color=Color.dark_green())

    @commands.Cog.listener()
    async def on_ready(self):
        self.get_channels()
        print(f"{self.bot.user.name}#{self.bot.user.discriminator} online!")
        await self.bot.channels.k["Status"].send(embed = self.embed_constructor())


def setup(bot):
    cog = Log(bot)
    if bot.user:
        cog.get_channels()
    bot.add_cog(cog)
