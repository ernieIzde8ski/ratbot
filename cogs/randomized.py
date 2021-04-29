import json
from random import choice, randint, random, seed
from typing import Optional

import discord.ext.commands as commands


class Randomized(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.initialize())
        with open("configs/randomized.json", "r") as file:
            self.logged = json.load(file)

    async def initialize(self):
        await self.bot.wait_until_ready()
        self.bm_channel = self.bot.config.channels.bm

    @commands.command(aliases=["bM", "bm"])
    async def bM_meter(self, ctx, *, parameter: Optional[str]):
        """decides Based or Cringe"""
        # filter and truncate parameter
        parameter = parameter.replace("```", "Armenium") if parameter else "Your"
        parameter = parameter[:1000] + (parameter[1000:] and "[…]")
        # set seed so that bot decides consistently
        seed(self.bot.static.remove_strange_chars(parameter.lower()))
        # decide if based or cringe
        bc_decision = choice(["Based", "Cringe"])
        punctuation_ending = choice(["!", "."]) * randint(1, 8)
        # send response
        await ctx.send(f"**{parameter}** are **{bc_decision}**{punctuation_ending}")
        # truncate response again
        parameter = parameter[:250] + (parameter[250:] and "[…]")
        # log response if not already logged
        if parameter.lower() in self.logged:
            return
        await self.bm_channel.send(f"```\n{parameter}, {bc_decision}{punctuation_ending}\n```")
        with open("configs/randomized.json", mode="w") as f:
            self.logged.append(parameter.lower())
            json.dump(self.logged, f)

    @commands.command(aliases=["gm", "gobi", "choochie"])
    async def gobi_meter(self, ctx, *, phrase: str):
        """Determines what percent gobi something is"""
        seed(self.bot.static.remove_strange_chars(phrase.lower()))
        percent = round(random() * 100, 1)
        await ctx.channel.send(f"\"{phrase}\" is {percent}% Gobi")

    @commands.command(aliases=["song", "rs"])
    async def random_song(self, ctx):
        """Pulls a random song from the configuration file"""
        await ctx.channel.send(f"https://youtu.be/{choice(ctx.bot.config.songs)}")

    @commands.command(aliases=["choose"])
    async def decide(self, ctx, *, _list: str):
        """choose item from a list separated by commas"""
        await ctx.channel.send(f"i Choose `{choice(_list.split(', '))}`")


def setup(bot):
    bot.add_cog(Randomized(bot))
