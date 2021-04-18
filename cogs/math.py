from typing import Union

import discord.ext.commands as commands


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def mean(ints):
        if len(ints) > 0:
            return f"{sum(ints)}/{len(ints)}={sum(ints) / len(ints)}"

    @commands.command(aliases=["l"])
    async def list_stats(self, ctx, *, lista: Union[list, tuple]):
        mean = self.mean(lista)
        return await ctx.channel.send(mean)


def setup(bot):
    bot.add_cog(Math(bot))
