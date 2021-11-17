from discord import Forbidden, HTTPException
from discord.ext import commands
from typing import Optional, Union

from modules.converters import FlagConverter


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def echo(self, ctx, messageable: Optional[Union[commands.UserConverter, commands.TextChannelConverter]], *, message: str):
        """Echo a message
        Optional parameter messageable determines location"""
        if not messageable:
            messageable = ctx
        if message[:1] == "\\":
            message = message[1:]
        try:
            await messageable.send(message)
        except (Forbidden, HTTPException) as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("pong")

    @commands.command(hidden=True)
    async def flags(self, ctx, *, flags: Optional[FlagConverter]):
        """Return flags"""
        if not flags:
            await ctx.send("No flags present")
        else:
            await ctx.send(f"Flags: {flags}")

    @commands.command(hidden=True)
    async def songs(self, ctx):
        """Return the entire song list"""
        await ctx.send(self.bot.songs)


def setup(bot):
    bot.add_cog(Ping(bot))
