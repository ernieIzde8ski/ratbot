from pytz import timezone
from datetime import datetime

from discord.ext import commands


async def now(armenium: bool):
    if armenium:
        return str(datetime.now(tz=timezone("America/Los_Angeles")).strftime("%m-%d-%Y %H:%M:%S"))
    else:
        return str(datetime.now(tz=timezone("America/New_York")).strftime("%d-%m-%Y %H:%M:%S"))


class Timekeeping(commands.Cog):
    """Keeps time"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["time", "now", "EST", "est"])
    async def based_time(self, ctx):
        """Tells the Ernie Standard Time"""
        await ctx.send(f"it's {await now(False)} in EST (Ernie Standard Time)")
        return

    @commands.command(aliases=["bitchtime", "PST", "pst", "cst"])
    async def bitch_time(self, ctx):
        """Tells the Cringe standard time"""
        await ctx.send(f"it's {await now(True)} in PST (Plebeian Standard Time)")


def setup(bot):
    bot.add_cog(Timekeeping(bot))
