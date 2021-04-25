import discord.ext.commands as commands


class Fun(commands.Cog):
    """Miscellaneous drivellous commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["CC", "cc"])
    async def cringecount(self, ctx, iteration: int = 1):
        """\"Liking liking things is cringe is cringe\""""
        if iteration > 100: return await ctx.channel.send("no")
        await ctx.send(f"Bro.... Liking {'“Liking ' * iteration}Things {'Is Cringe” ' * iteration}is Cringe....")


def setup(bot):
    bot.add_cog(Fun(bot))
