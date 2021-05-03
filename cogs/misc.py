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

    @commands.command(aliases=["mogus", '"Among Us" Funny Comic Meme'])
    async def amogus(self, ctx):
        amogus = "https://cdn.discordapp.com/attachments/544857539607789574/838602527230263306/qn5v4syty9r61.png"
        await ctx.send(amogus)


def setup(bot):
    bot.add_cog(Fun(bot))
