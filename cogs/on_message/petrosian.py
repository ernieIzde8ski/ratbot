import re
from json import load
from random import random

from discord import AllowedMentions, Message
from discord.ext import commands


class Petrosian(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.regex = r"pipi|liers|petr(o|at)s[iy]an|looser|\"w\"esley\"s\"o|firouzja|otbblitzmatch"
        with open("modules/JSON/petrosian.json", "r", encoding="utf-8") as file:
            self.petrosian = load(file)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if message.author.bot:
            return
        elif message.guild:
            if str(message.guild.id) in self.bot.pipi_guilds:
                return

        if not re.search(self.regex, message.content, re.ASCII + re.IGNORECASE):
            return
        elif random() > 0.33:
            return
        else:
            await message.author.send(self.petrosian.format(message.author.mention),
                                      allowed_mentions=AllowedMentions.all())


def setup(bot):
    bot.add_cog(Petrosian(bot))
