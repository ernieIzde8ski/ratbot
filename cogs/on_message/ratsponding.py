import discord.ext.commands as commands


class Ratsponding(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def rat(self, message):
        if message.guild:
            # prune non rat messages in #rat channels
            if message.channel.name == "rat" and message.content != "rat":
                await message.delete()
                return
        if message.author.bot:
            return
        elif message.content.startswith("rat"):
            if message.content.startswith("rather"): return
            await message.channel.send("rat")
            log = f"[{self.bot.static.now()}] rat from {message.author} in "
            log += "dms" if not message.guild else str(message.guild)
            print(log)

    @commands.Cog.listener("on_message")
    async def trolfl(self, message):
        if message.author.bot or not message.content: return
        if "troll" in message.content.lower(): await message.add_reaction("<:trolled:846670001691557938>")


def setup(bot):
    bot.add_cog(Ratsponding(bot))
