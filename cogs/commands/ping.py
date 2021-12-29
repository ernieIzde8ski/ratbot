from discord import Forbidden, HTTPException
from discord.abc import Messageable
from discord.ext import commands
from typing import Optional
from utils.classes import RatBot

from utils.converters import FlagConverter


class Ping(commands.Cog):
    def __init__(self, bot: RatBot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def echo(self, ctx: commands.Context, messageable: Optional[Messageable], *, message: str):
        """Echo a message
        Optional parameter messageable determines location"""
        messageable = messageable or ctx
        if message.startswith("\\"):
            message = message[1:]
        try:
            await messageable.send(message)
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
