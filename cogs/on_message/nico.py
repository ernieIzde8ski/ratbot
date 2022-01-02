from datetime import datetime
import discord
from discord.abc import User

from discord.ext import commands
from fuzzywuzzy import fuzz

from utils.classes import RatBot


class Nico(commands.Cog):
    Nico: discord.User

    def __init__(self, bot: RatBot):
        self.bot = bot
        self.time = None

    async def get_nico(self) -> None:
        await self.bot.wait_until_ready()
        self.Nico = self.bot.get_user(251792286260658196)

    @staticmethod
    def verify(s1: str, s2: str = "frick", min: int = 65):
        s1 = s1.lower()
        s2 = s2.lower()
        return fuzz.ratio(s1, s2) > min or fuzz.partial_ratio(s1, s2) > (min + 10)

    @commands.Cog.listener()
    async def on_message(self, message):
        # ignore incorrect channels/authors, failing grades
        if message.channel.id != 758373055918899216 or message.author.id != 544274326002860033:
            return
        elif not self.verify(message.content):
            return

        now = datetime.now().strftime("%Y-%m-%d;%H:%M")
        if self.time == now:
            return

        await self.Nico.send("<#758373055918899216>")
        self.time = now


def setup(bot: RatBot):
    cog = Nico(bot)
    bot.loop.create_task(cog.get_nico())
    bot.add_cog(cog)
