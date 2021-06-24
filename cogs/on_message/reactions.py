from random import random, choice
from typing import Iterable
from discord.errors import Forbidden
from discord.ext import commands
from modules.json import safe_load


class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trolls = safe_load("data/trolls.json", ["🚎"])
        self.lmfao = safe_load("data/lmfao.json", "🤬")

    @staticmethod
    def strings_in(string: str, substrings: Iterable, ignore_case: bool = True):
        if ignore_case:
            string = string.lower()
            substrings = [substring.lower() for substring in substrings]
        for substring in substrings:
            if substring in string:
                return True
        else:
            return False

    @commands.Cog.listener("on_message")
    async def on_troll(self, message):
        if not self.strings_in(message.content, ["troll", "trole", "troling"]):
            return
        try:
            troll = choice(self.trolls)
            await message.add_reaction(troll)
        except Forbidden:
            await message.channel.send("Trolled")

    @commands.Cog.listener("on_message")
    async def on_lmfao(self, message):
        if random() > 0.15 or not self.strings_in(message.content, ["lmao", "lmfao"]):
            return

        try:
            await message.add_reaction(self.lmfao)
        except Forbidden:
            await message.channel.send("Lmao !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


def setup(bot):
    bot.add_cog(Reactions(bot))
