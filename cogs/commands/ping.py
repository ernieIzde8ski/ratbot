from typing import Optional, Union
import discord
from discord.ext import commands
from utils import FlagConverter, RatCog


Messageable = Union[discord.Member, discord.TextChannel, discord.User]


class Ping(RatCog):
    """Testing commands"""

    @commands.command()
    @commands.is_owner()
    async def echo(self, ctx: commands.Context, messageable: Optional[Messageable], *, message: str):
        """Echo a message
        Optional parameter messageable determines target"""
        target = messageable or ctx
        message = message.removeprefix("\\")
        try:
            await target.send(message)
        except (discord.Forbidden, discord.HTTPException) as e:
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
        resp = str(self.bot.settings.songs)
        if len(resp) > 1500:
            resp = self.bot.settings.songs.keys()
        await ctx.send(", ".join(resp))


setup = Ping.basic_setup
