import discord
from discord.ext import commands
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

    @commands.hybrid_command()
    @commands.is_owner()
    async def echo(self, ctx: RatCtx, channel: discord.TextChannel | None = None, *, message: str):
        await (channel or ctx.channel).send(message)

setup = TestCog.basic_setup
