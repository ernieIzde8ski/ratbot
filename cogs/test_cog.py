from discord.ext import commands
from discord import app_commands
from utils import RatCog, RatCtx


class TestCog(RatCog):
    @commands.hybrid_command()
    async def ping(self, ctx: RatCtx) -> None:
        """a test command"""
        await ctx.send("pong")

    @commands.hybrid_command()
    @commands.is_owner()
    async def error(self, ctx: RatCtx):
        raise RuntimeError("get fucked")


setup = TestCog.basic_setup
