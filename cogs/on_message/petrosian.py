import re
from json import load
from random import random

from discord import AllowedMentions, Message
from discord.ext import commands

from utils.classes import RatBot


class Petrosian(commands.Cog):
    def __init__(self, bot: RatBot):
        self.bot = bot
        self.regex = re.compile(r"pipi|liers|petr(o|at)s[iy]an|looser|\"w\"esley\"s\"o|firouzja|otbblitzmatch", re.ASCII + re.IGNORECASE)
        with open("utils/JSON/petrosian.json", "r", encoding="utf-8") as file:
            self.petrosian = load(file)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        elif message.guild:
            if str(message.guild.id) in self.bot.data.pipi_guilds:
                return

        if not re.search(self.regex, message.content):
            return
        elif random() > 0.33:
            return
        else:
            await message.author.send(self.petrosian.format(message.author.mention),
                                      allowed_mentions=AllowedMentions.all())


def setup(bot: RatBot):
    bot.add_cog(Petrosian(bot))
