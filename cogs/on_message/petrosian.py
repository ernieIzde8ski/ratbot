from discord.ext import commands
from discord import AllowedMentions
from random import random
from re import match
from json import load


class Petrosian(commands.Cog):
    def __init__(self):
        self.regex = r"pipi|liers|petr(o|at)s[iy]an|looser|\"w\"esley\"s\"o|firouzja|otbblitzmatch"
        with open("modules/petrosian.json", "r", encoding="utf-8") as file:
            self.petrosian = load(file)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        text = "".join(message.content.lower().split())
        if not match(self.regex, text):
            return
        elif random() > 0.33:
            return
        else:
            await message.author.send(self.petrosian.format(message.author.mention), allowed_mentions = AllowedMentions.all())
        
def setup(bot):
    bot.add_cog(Petrosian())