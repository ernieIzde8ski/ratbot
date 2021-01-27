from datetime import datetime
from typing import Union

import discord
import discord.ext.commands as commands


def now():
    return str(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))


class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # i didn't write any of the following lines xddddddddd
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, *, module):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, *, module):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, *, module):
        """Reloads a module."""
        try:
            self.bot.reload_extension(module)
        except commands.ExtensionError as e:
            await ctx.send(f'{e.__class__.__name__}: {e}')
        else:
            await ctx.send('\N{OK HAND SIGN}')

    @commands.command(aliases=['echo', 'wessel'])
    @commands.is_owner()
    async def vessel(self, ctx, messageable: Union[commands.TextChannelConverter, commands.UserConverter, int, None], *,
                     text: str):
        """Standard echo command"""
        if type(messageable) is int or not messageable:
            messageable = self.bot.get_channel(messageable) if (type(messageable) is int) else ctx.channel
        await messageable.send(text)


def setup(bot):
    bot.add_cog(Administration(bot))
