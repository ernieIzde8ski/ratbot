from datetime import datetime
from typing import Union
from sys import exit
from pytz import timezone

import discord
import discord.ext.commands as commands


from config import statusChannel


def now():
    return str(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))


class Administration(commands.Cog):
    """no run if not admin ok"""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.bot.user} has connected to Discord!")
        log_channel = self.bot.get_channel(statusChannel)
        await log_channel.send(embed=discord.Embed(title="<:online:708885917133176932> online!",
                                                   timestamp=datetime.now(tz=timezone("America/New_York")),
                                                   color=discord.Color.green()))

    # i stole the following lines up until wessel Xd
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

    @commands.command(aliases=["die", "off"])
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shut down the bot and whole script Lol"""
        await ctx.channel.send("Ok")
        log_channel = self.bot.get_channel(statusChannel)
        await log_channel.send(embed=discord.Embed(title="<:offline:708886391672537139> shutting Down.....",
                                                   timestamp=ctx.message.created_at,
                                                   color=discord.Color.dark_red()))
        exit()


def setup(bot):
    bot.add_cog(Administration(bot))
