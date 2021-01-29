from discord.ext import commands

corrections_list = ("bano", "Baño"), ("senor", "Señor"), ("senora", "Señora"), ("jalapeno", "Jalapeño"), (
                    "canada", "Cañada"), ("canadian", "Cañadian")


class Corrections(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if message.guild and message.channel.name == "rat": return
        message_list = message.content.lower().split(" ")
        for x, y in corrections_list:
            if x in message_list:
                return await message.channel.send(f"did you mean: {y}")


def setup(bot):
    bot.add_cog(Corrections(bot))
