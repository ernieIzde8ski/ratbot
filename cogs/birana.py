"""
just to be Absolutely clear
i do not actually intend on running this because i don't want ratbot banned
some idiot just kept pestering me for it
is currently untested
"""
from discord.ext import commands


class Birana(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.check(lambda c: False)
    async def birana(self, ctx):
        """Sends the birana response message in all channels the bot has access to
        the command check always returns False"""
        for guild in self.bot.guilds:
            for channel in guild.channels:
                await channel.send(
                    """SHUT THE FUCK UP ARMENIUM , WHAT WOULD YOU KNOW ABOUT WHETHER A WORD IS FUNNY OR NOT ? YOU KNOWING OF NOTHING !!! YOU ARE STUPID , STUPID LITTLE CRYBABY KID , WHO LIFT THE 50 TIME 15 BOUND (VERY LITTLE WEIGHT , VERY LUGHT) , YOU ARE WEAK , AND PAINFUL , IT SUCKS TO BE YOU !!! "AREMENIAUM" IS A SCHIT, SUCK COUNTRY BUILT OF BAD AND TERRIBLE KIDS , LIKE YOU RSELF, YOUR CULTURE SUCK, YOUR HERITAGE, , IT IS BAD ,AND YOUR CHOICE ??? TERRIBLE ABSOLUTE LY WAFUL. "BIRANA" WELL DESCRIBES THE ABSOLUTE DIFFERENCE OSPOSITE OF YOU, AND YOUR EVERY THING , BECAUSE "BIRANA" BAED YOU ARE CIRNGE. BIRANA "BASED" YOU ARE "CRINGE".""")
        else:
            await ctx.send("Done")
            await ctx.send("birana!!!!!!!!")

    @birana.command(aliases=["arm", "armenium"])
    async def Armenium(self, ctx):
        """Sends the birana response message"""
        await ctx.send(
            """SHUT THE FUCK UP ARMENIUM , WHAT WOULD YOU KNOW ABOUT WHETHER A WORD IS FUNNY OR NOT ? YOU KNOWING OF NOTHING !!! YOU ARE STUPID , STUPID LITTLE CRYBABY KID , WHO LIFT THE 50 TIME 15 BOUND (VERY LITTLE WEIGHT , VERY LUGHT) , YOU ARE WEAK , AND PAINFUL , IT SUCKS TO BE YOU !!! "AREMENIAUM" IS A SCHIT, SUCK COUNTRY BUILT OF BAD AND TERRIBLE KIDS , LIKE YOU RSELF, YOUR CULTURE SUCK, YOUR HERITAGE, , IT IS BAD ,AND YOUR CHOICE ??? TERRIBLE ABSOLUTE LY WAFUL. "BIRANA" WELL DESCRIBES THE ABSOLUTE DIFFERENCE OSPOSITE OF YOU, AND YOUR EVERY THING , BECAUSE "BIRANA" BAED YOU ARE CIRNGE. BIRANA "BASED" YOU ARE "CRINGE".""")

    @birana.command(aliases=["real", "birana"])
    async def true(self, ctx):
        """returns 'birana'"""
        await ctx.send("birana")


def setup(bot):
    bot.add_cog(Birana(bot))
