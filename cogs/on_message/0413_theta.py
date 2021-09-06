import discord
from discord.ext import commands
from fuzzywuzzy import fuzz


class AEBDTheta(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == 304118384663068673 and message.channel.id == 884237172717277225:
            if fuzz.ratio(message.content.lower(), "**daily 'armenium' fact**") > 85:
                return
            await message.channel.edit(topic=(message.channel.topic+"\n"+message.content))


def setup(bot: commands.Bot) -> None:
    bot.add_cog(AEBDTheta(bot))
