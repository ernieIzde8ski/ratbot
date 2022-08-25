from discord.ext import commands
from utils import RatCog, RatCtx


class TestCog(RatCog):
    @commands.hybrid_command()
    async def ping(self, ctx: RatCtx) -> None:
        """a test command"""
        await ctx.channel.send("pong")


setup = TestCog.basic_setup
