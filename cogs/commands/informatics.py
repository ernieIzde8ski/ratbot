from discord.ext import commands
from utils import RatCog, RatCtx


class Informatics(RatCog):
    @commands.hybrid_command(aliases=["info"])
    async def invite(self, ctx: RatCtx):
        await ctx.send("")

    async def setup_hook(self):
        raise RuntimeError("Get fucked")


setup = Informatics.basic_setup
