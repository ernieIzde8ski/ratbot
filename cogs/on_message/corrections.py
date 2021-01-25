import discord
import discord.ext.commands as commands
corrections_list = ("bano", "Baño"), ("senor", "Señor"), ("senora", "Señora"), ("jalapeno", "Jalapeño"), ("canada", "Cañada"), ("canada", "Cañadian")

class corrections(commands.Cog):
    def __init__(self, bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:  return
        if message.guild and message.channel.name == "rat": return
        message_list = message.content.lower().split(" ")
        list = []
        for x, y in corrections_list:
            if x in message_list:
                return await message.channel.send(f"did you mean: {y}")

def setup(bot):
    bot.add_cog(corrections(bot))
