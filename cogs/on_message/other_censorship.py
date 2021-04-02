from discord.ext import commands


class GoingToPutMoreFeaturesInMainBotFile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == 159985870458322944 and message.guild.id == 526207286067068928:
            if "you just advanced" in message.content:
                await message.delete()
        if message.author.bot: return
        # respond when anyone says my name
        if "ernie reads star trek fanfics" in message.content.lower():
            await message.delete()
        elif "ernie does not read star trek fanfics" in message.content.lower():
            await message.channel.send("True")


def setup(bot):
    bot.add_cog(GoingToPutMoreFeaturesInMainBotFile(bot))
