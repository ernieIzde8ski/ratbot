import discord.ext.commands as commands
from discord import Game


class Stati(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.initialize())

    async def initialize(self):
        await self.bot.wait_until_ready()
        status = Game(f"prefix is {self.bot.config.prefix}")
        await self.bot.change_presence(activity=status)

    @commands.command(aliases=["status", "set_status"])
    @commands.is_owner()
    async def change_status(self, ctx, *, status):
        """Sets the bot's status"""
        await self.bot.change_presence(activity=Game(status))
        await ctx.send(f"set the presence to `{status}`")


def setup(bot):
    bot.add_cog(Stati(bot))
