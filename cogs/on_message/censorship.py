from discord.ext import commands
import re

class Censorship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def reduce(text: str) -> str:
        text = "".join(text.lower().split())
        text = "".join([c for c in text if ord(c) <= 128])
        return text

    @commands.Cog.listener("on_message")
    async def on_twitter(self, message):
        if not message.guild:
            return
        elif self.bot.config["main_guild"] != message.guild.id:
            return
        elif message.author.id == 368780147563823114 and "twitter" in self.reduce(message.content):
            await message.delete()
            await message.author.send("Trolled")
    
    @commands.Cog.listener("on_message")
    async def on_fanfics(self, message):
        if message.author.bot or not message.guild:
            return
        message.content = self.reduce(message.content)
        if re.match(r"(ernie|ernest)readsstartrekfanfic(tion|)(s|)", message.content):
            await message.delete()
        elif re.match(r"(ernie|ernest)(doesnot|doesn't)readstartrekfanfic(tion|)(s|)", message.content):
            await message.reply("Based !!!!!!!!!!!!")
        


def setup(bot):
    bot.add_cog(Censorship(bot))
