from modules._json import safe_load, safe_dump
from typing import Optional, Union
from discord.ext import commands
from datetime import datetime
from pytz import timezone


class Miscellaneous(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = safe_load("data/timekeeping.json", {})

    @commands.command()
    async def birana(self, ctx, armenium: str = "ARMENIUM", armeniaum: str = "AREMENIAUM"):
        """Return the Birana copypasta"""
        await ctx.send('SHUT THE FUCK UP {armenium} , WHAT WOULD YOU KNOW ABOUT WHETHER A WORD IS FUNNY OR NOT ? YOU KNOWING OF NOTHING !!! YOU ARE STUPID , STUPID LITTLE CRYBABY KID , WHO LIFT THE 50 TIME 15 BOUND (VERY LITTLE WEIGHT , VERY LUGHT) , YOU ARE WEAK , AND PAINFUL , IT SUCKS TO BE YOU !!! "{armeniaum}" IS A SCHIT, SUCK COUNTRY BUILT OF BAD AND TERRIBLE KIDS , LIKE YOU RSELF, YOUR CULTURE SUCK, YOUR HERITAGE, , IT IS BAD ,AND YOUR CHOICE ??? TERRIBLE ABSOLUTE LY WAFUL. "BIRANA" WELL DESCRIBES THE ABSOLUTE DIFFERENCE OSPOSITE OF YOU, AND YOUR EVERY THING , BECAUSE "BIRANA" BAED YOU ARE CIRNGE. BIRANA "BASED" YOU ARE "CRINGE".'.format(armenium=armenium, armeniaum=armeniaum))

    @commands.group(invoke_without_command=True, aliases=["now"])
    async def time(self, ctx, *, tz: Optional[Union[timezone, str]]):
        """Return the current time
        Returns the time based off either a given or set timezone"""
        if not tz:
            id = str(ctx.author.id)
            if self.data.get(id):
                tz = timezone(self.data[id])
            else:
                tz = timezone(self.bot.config["preferred_timezone"])
        elif isinstance(tz, str):
            return await ctx.send("Invalid timezone!\n"
                                  "A valid list is available here: "
                                  "<https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568>")

        now = datetime.now(tz=tz)
        await ctx.send(now.strftime(f"It's currently `%Y-%m-%d, %H:%M:%S` in the timezone `{tz}`."))

    @time.command()
    async def set(self, ctx, *, tz: Optional[timezone]):
        """Sets a PYTZ-compatible timezone
        Valid timezones are at available at
        https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568"""
        if not tz:
            return await ctx.send("Invalid timezone!\n"
                                  "A valid list is available here: "
                                  "<https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568>")
        tz = tz.__str__()
        self.data[str(ctx.author.id)] = tz
        safe_dump("data/timekeeping.json", self.data)
        await ctx.send(f"Set your timezone to {tz}")


def setup(bot):
    bot.add_cog(Miscellaneous(bot))
