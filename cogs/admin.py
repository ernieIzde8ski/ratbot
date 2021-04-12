from datetime import datetime
from sys import exit

import discord
import discord.ext.commands as commands
from pytz import timezone


class Administration(commands.Cog):
    """no run if not admin ok"""

    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.initialize())

    async def initialize(self):
        await self.bot.wait_until_ready()
        self.bot.config.channels._get_channels(self.bot)
        print(f"{self.bot.user} has connected to Discord!")
        await self.bot.config.channels.status.send(embed=discord.Embed(
            title="<:online:708885917133176932> online!",
            timestamp=datetime.now(
                tz=timezone("America/New_York")
            ),
            color=discord.Color.green())
        )

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
            print(f"loaded {module}")

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
            print(f"unloaded {module}")

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
            print(f"reloaded {module}")

    @commands.command(aliases=["die", "off"])
    @commands.is_owner()
    async def shutdown(self, ctx):
        """Shut down the bot and whole script Lol"""
        await ctx.channel.send("Ok")
        await ctx.bot.config.channels.status.send(
            embed=discord.Embed(title="<:offline:708886391672537139> shutting Down.....",
                                timestamp=ctx.message.created_at,
                                color=discord.Color.dark_red())
        )
        exit()


def setup(bot):
    bot.add_cog(Administration(bot))
