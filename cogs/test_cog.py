from discord.ext import commands
from utils import RatCog, RatCtx


class TestCog(RatCog):
    @commands.command()
    async def ping(self, ctx: RatCtx) -> None:
        await ctx.channel.send("pong")


setup = TestCog.basic_setup
