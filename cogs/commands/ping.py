from typing import Optional

from discord import Forbidden, HTTPException, Member, TextChannel, User
from discord.ext import commands
from utils.classes import RatBot, RatCog
from utils.converters import FlagConverter


class Ping(RatCog):
    """Testing commands"""

    @commands.command()
    @commands.is_owner()
    async def echo(self, ctx: commands.Context, messageable: Optional[Member | TextChannel | User], *, message: str):
        """Echo a message
        Optional parameter messageable determines target"""
        target = messageable or ctx
        message = message.removeprefix("\\")
        try:
            await target.send(message)
        except (Forbidden, HTTPException) as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("pong")

    @commands.command(hidden=True)
    async def flags(self, ctx: commands.Context, *, flags: Optional[FlagConverter]):
        """Return flags"""
        if not flags:
            await ctx.send("No flags present")
        else:
            await ctx.send(f"Flags: {flags}")

    @commands.command(hidden=True)
    async def songs(self, ctx: commands.Context):
        """Return the entire song list"""
        await ctx.send(self.bot.data.songs)


def setup(bot: RatBot):
    bot.add_cog(Ping(bot))
