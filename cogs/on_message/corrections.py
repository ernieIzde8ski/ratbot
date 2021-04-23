import discord.ext.commands as commands


class Corrections(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if message.guild and message.channel.name == "rat": return
        for word in message.content.lower().split(" "):
            if word in self.bot.config.corrections.keys():
                return await message.channel.send(f"did you mean: {self.bot.config.corrections.get(word)}")


def setup(bot):
    bot.add_cog(Corrections(bot))
