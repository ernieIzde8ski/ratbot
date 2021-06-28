from modules._json import safe_load, safe_dump
from typing import Optional, Union
from discord.ext import commands
from datetime import datetime
from pytz import timezone


class Timekeeping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = safe_load("data/timekeeping.json", {})

    @commands.group(invoke_without_command=True, aliases=["now"])
    async def time(self, ctx, *, tz: Optional[Union[timezone, str]]):
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
        if not tz:
            return await ctx.send("Invalid timezone!\n"
                                  "A valid list is available here: "
                                  "<https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568>")
        tz = tz.__str__()
        self.data[str(ctx.author.id)] = tz
        safe_dump("data/timekeeping.json", self.data)
        await ctx.send(f"Set your timezone to {tz}")


def setup(bot):
    bot.add_cog(Timekeeping(bot))
