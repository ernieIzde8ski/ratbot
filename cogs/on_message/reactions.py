import re
from random import choice, random

from discord import Forbidden, Message
from discord.ext import commands
from utils import RatCog


LaughPattern = re.compile(r"lmf?ao", re.IGNORECASE)
TrollPattern = re.compile(r"trol(l|i|e)", re.IGNORECASE)


class Reactions(RatCog):
    """Reactions to messages with troll/laughing emojis"""

    @commands.Cog.listener()
    async def on_message(self, message: Message):

        if re.search(TrollPattern, message.content):
            try:
                await message.add_reaction(choice(self.emojis.trolls))
            except Forbidden:
                if message.author == self.bot.user:
                    return
                await message.channel.send("Trolled")

        if re.search(LaughPattern, message.content):
            if random() > 0.02:
                return
            try:
                await message.add_reaction(self.emojis.laugh)
            except Forbidden:
                await message.channel.send("Lmao !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


setup = Reactions.basic_setup
