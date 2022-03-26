from datetime import datetime

import discord
from discord.ext import commands
from fuzzywuzzy import fuzz
from utils import RatCog


class Nico(RatCog):
    nico: discord.User
    time: str | None = None

    async def _on_ready(self) -> None:
        nico = self.bot.get_user(251792286260658196)
        if nico is None:
            raise discord.DiscordException("Nico not found :(")
        self.nico = nico

    @staticmethod
    def verify(s1: str, s2: str = "frick", min: int = 65):
        s1 = s1.lower()
        s2 = s2.lower()
        return fuzz.ratio(s1, s2) > min or fuzz.partial_ratio(s1, s2) > (min + 10)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # ignore incorrect channels/authors, failing grades
        if message.channel.id != 758373055918899216 or message.author.id != 544274326002860033:
            return
        elif not self.verify(message.content):
            return

        now = datetime.now().strftime("%Y-%m-%d;%H:%M")
        if self.time == now:
            return

        await self.nico.send("<#758373055918899216>")
        self.time = now


setup = Nico.basic_setup
