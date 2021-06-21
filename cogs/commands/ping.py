from typing import Optional
from discord.ext import commands
from modules.converters import FlagConverter


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Ping = None

    @commands.command()
    async def flags(self, ctx, *, flags: Optional[FlagConverter]):
        if not flags:
            await ctx.send("No flags present")
        else:
            await ctx.send(f"Flags: {flags}")


def setup(bot):
    bot.add_cog(Ping(bot))
