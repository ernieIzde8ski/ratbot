import discord.ext.commands as commands


class Corrections(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.corrections_list = [
            ("bano", "Baño"),
            ("senor", "Señor"),
            ("senora", "Señora"),
            ("jalapeno", "Jalapeño"),
            ("canada", "Cañada"),
            ("canadian", "Cañadian"),
            ("retard", "Ratard"),
            ("ExampleSlur", "Armenium")
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if message.guild and message.channel.name == "rat": return
        message_list = message.content.lower().split(" ")
        for x, y in self.corrections_list:
            if x.lower() in message_list:
                return await message.channel.send(f"did you mean: {y}")


def setup(bot):
    bot.add_cog(Corrections(bot))
