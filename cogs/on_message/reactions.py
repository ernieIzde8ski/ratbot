from random import random, choice
from discord import Forbidden, Message
from discord.ext import commands
from modules._json import safe_load
import re


class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.trolls = safe_load("data/trolls.json", ["🚎"])
        self.lmfao = safe_load("data/lmfao.json", "🤬")

    @commands.Cog.listener("on_message")
    async def on_troll(self, message: Message):
        if not re.search(r"troll|trole|troling", message.content, re.I):
            return
        try:
            troll = choice(self.trolls)
            await message.add_reaction(troll)
        except Forbidden:
            if message.author == self.bot.user:
                return
            await message.channel.send("Trolled")

    @commands.Cog.listener("on_message")
    async def on_lmfao(self, message: Message):
        if random() > 0.15 or not re.match(r"(?i)lmf?ao", message.content):
            return

        try:
            await message.add_reaction(self.lmfao)
        except Forbidden:
            await message.channel.send("Lmao !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


def setup(bot):
    bot.add_cog(Reactions(bot))
