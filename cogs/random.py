import random
from config import songs, bmChannel
from config import songs, bmChannel

import discord.ext.commands as commands
from typing import Optional


class Randomized(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self._get_channel())

    async def _get_channel(self):
        await self.bot.wait_until_ready()
        self.bmChannel = self.bot.get_channel(bmChannel)

    @commands.command(aliases=["bM", "bm"])
    async def bM_meter(self, ctx, *, option: Optional[str]):
        """decides Based or Cringe"""
        option = option.replace("```", "Armenium") if option else "Your"
        random.seed(option.lower())
        bc_decision = random.choice(["Based", "Cringe"])
        punctuation_ending = random.choice([random.choice(("!", ".")) * x for x in range(1, 8)])
        await ctx.send(f"**{option}** are **{bc_decision}**{punctuation_ending}")
        await self.bmChannel.send("```"
                                  f"{option}, {bc_decision}{punctuation_ending}   [{ctx.message.created_at}]"
                                  "```")

    @commands.command(aliases=["song", "rs"])
    async def random_song(self, ctx):
        """Pulls a random song from the configuration file"""
        await ctx.channel.send(f"https://youtu.be/{random.choice(songs)}")

    @commands.command()
    async def decide(self, ctx, *, _list: str):
        """choose item from a list separated by forward slashes"""
        await ctx.channel.send(f"i Choose `{random.choice(_list.split(' / '))}`")


def setup(bot):
    bot.add_cog(Randomized(bot))
