import re
from random import choice, random

from discord import Forbidden, Message
from discord.ext import commands
from utils.classes import RatBot
from utils.functions import safe_load


class Reactions(commands.Cog):
    def __init__(self, bot: RatBot):
        self.bot = bot
        self.lmfao = safe_load("data/lmfao.json", "🤬")
        self.lmagex = re.compile("lmf?ao", re.I)

    @commands.Cog.listener()
    async def on_message(self, message: Message):

        if re.search(self.bot.data.trollgex, message.content):
            try:
                await message.add_reaction(choice(self.bot.data.trolljis))
            except Forbidden:
                if message.author == self.bot.user:
                    return
                await message.channel.send("Trolled")

        if re.search(self.lmagex, message.content):
            if random() > 0.01:
                return
            try:
                await message.add_reaction(self.lmfao)
            except Forbidden:
                await message.channel.send("Lmao !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


def setup(bot: RatBot):
    bot.add_cog(Reactions(bot))
