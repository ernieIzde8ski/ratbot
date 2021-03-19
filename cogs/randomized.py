from typing import Optional

import discord.ext.commands as commands

import random


class Randomized(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.initialize())

    async def initialize(self):
        await self.bot.wait_until_ready()
        self.bm_channel = self.bot.config.channels.bm

    @commands.command(aliases=["bM", "bm"])
    async def bM_meter(self, ctx, *, option: Optional[str]):
        """decides Based or Cringe"""
        option = option.replace("```", "Armenium") if option else "Your"
        random.seed(option.lower())
        bc_decision = random.choice(["Based", "Cringe"])
        punctuation_ending = random.choice([random.choice(("!", ".")) * x for x in range(1, 8)])
        await ctx.send(f"**{option}** are **{bc_decision}**{punctuation_ending}")
        await self.bm_channel.send("```"
                                   f"{option}, {bc_decision}{punctuation_ending}   [{ctx.message.created_at}]"
                                   "```")

    @commands.command(aliases=["song", "rs"])
    async def random_song(self, ctx):
        """Pulls a random song from the configuration file"""
        await ctx.channel.send(f"https://youtu.be/{random.choice(ctx.bot.config.songs)}")

    @commands.command()
    async def decide(self, ctx, *, _list: str):
        """choose item from a list separated by forward slashes"""
        await ctx.channel.send(f"i Choose `{random.choice(_list.split(' / '))}`")


def setup(bot):
    bot.add_cog(Randomized(bot))