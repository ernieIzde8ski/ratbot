from discord.ext import commands
from fuzzywuzzy import fuzz
from modules.functions import reduce
import re


class Censorship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def on_twitter(self, message):
        if not message.guild:
            return
        elif self.bot.config["main_guild"] != message.guild.id:
            return
        content = reduce(message.content)
        if fuzz.partial_ratio(content, "twiter") > 75:
            await message.delete()
            await message.author.send("Trolled")

    @commands.Cog.listener("on_message")
    async def on_fanfics(self, message):
        if message.author.bot or not message.guild:
            return
        content = reduce(message.content)
        if re.match(r"(ernie|ernest)readsstartrekfanfic(tion|)(s|)", content):
            await message.delete()
        elif re.match(r"(ernie|ernest)(doesnot|doesn't)readstartrekfanfic(tion|)(s|)", content):
            await message.reply("Based !!!!!!!!!!!!")


def setup(bot):
    bot.add_cog(Censorship(bot))
