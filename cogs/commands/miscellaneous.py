from datetime import datetime

from discord.ext import commands
from pytz import BaseTzInfo, timezone
from utils import RatCog


class Miscellaneous(RatCog):
    """Random commands (but not randomized)"""

    @commands.command()
    async def birana(self, ctx: commands.Context, armenium: str = "ARMENIUM", armeniaum: str = "AREMENIAUM"):
        """Return the Birana copypasta"""
        await ctx.send(
            f'SHUT THE FUCK UP {armenium.upper()} , WHAT WOULD YOU KNOW ABOUT WHETHER A WORD IS FUNNY OR NOT ? YOU KNOWING OF NOTHING !!! YOU ARE STUPID , STUPID LITTLE CRYBABY KID , WHO LIFT THE 50 TIME 15 BOUND (VERY LITTLE WEIGHT , VERY LUGHT) , YOU ARE WEAK , AND PAINFUL , IT SUCKS TO BE YOU !!! "{armeniaum.upper()}" IS A SCHIT, SUCK COUNTRY BUILT OF BAD AND TERRIBLE KIDS , LIKE YOU RSELF, YOUR CULTURE SUCK, YOUR HERITAGE, , IT IS BAD ,AND YOUR CHOICE ??? TERRIBLE ABSOLUTE LY WAFUL. "BIRANA" WELL DESCRIBES THE ABSOLUTE DIFFERENCE OSPOSITE OF YOU, AND YOUR EVERY THING , BECAUSE "BIRANA" BAED YOU ARE CIRNGE. BIRANA "BASED" YOU ARE "CRINGE".'
        )

    @commands.command(aliases=["nsbm"])
    async def NSBM(self, ctx: commands.Context):
        await ctx.send("https://cdn.discordapp.com/attachments/404758309418172436/876620413701062727/ymq2us28roi61.png")

    @commands.group(invoke_without_command=True, aliases=["now"])
    async def time(self, ctx: commands.Context, *, tz: BaseTzInfo | str | None):
        """Return the current time
        Returns the time based off either a given or set timezone"""

        if tz is None:
            utz = self.users[ctx.author.id].tz
            tz = timezone(utz or self.config.tz)

        if isinstance(tz, str):
            raise commands.BadArgument(
                'Converting to "timezone" failed for parameter "tz". \n'
                "Valid timezone list: <https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568>"
            )

        now = datetime.now(tz=tz)
        await ctx.send(now.strftime(f"It's currently `%Y-%m-%d, %H:%M:%S` in the timezone `{tz}`."))

    @time.command()
    async def set(self, ctx: commands.Context, *, tz: timezone | None):
        # TODO: Allow for setting timezone to Discord
        """Sets a PYTZ-compatible timezone
        Valid timezones are at available at
        https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568"""
        if not tz:
            return await ctx.send(
                "Invalid timezone!\n"
                "A valid list is available here: "
                "<https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568>"
            )
        self.users[ctx.author.id].tz = str(tz)
        self.bot.settings.save()
        await ctx.send(f"Set your timezone to {tz}")


setup = Miscellaneous.basic_setup
