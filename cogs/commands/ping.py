from typing import Optional, Union
from discord.errors import Forbidden, HTTPException
from discord.ext import commands
from modules.converters import FlagConverter


class Ping(commands.Cog):
    def __init__(self):
        pass

    @commands.command()
    async def echo(self, ctx, messageable: Optional[Union[commands.UserConverter, commands.TextChannelConverter]], *, message: str):
        if not messageable:
            messageable = ctx
        if message[:1] == "\\":
            message = message[1:]
        try:
            await messageable.send(message)
        except (Forbidden, HTTPException) as e:
            await ctx.send(f"{e.__class__.__name__}: {e}")

    @commands.command(hidden=True)
    async def flags(self, ctx, *, flags: Optional[FlagConverter]):
        if not flags:
            await ctx.send("No flags present")
        else:
            await ctx.send(f"Flags: {flags}")


def setup(bot):
    bot.add_cog(Ping())
