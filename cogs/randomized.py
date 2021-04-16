import random
import json
from typing import Optional

import discord.ext.commands as commands


class Randomized(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self.initialize())
        async with open("configs/randomized.json", "r") as file:
            self.logged = json.load(file)

    async def initialize(self):
        await self.bot.wait_until_ready()
        self.bm_channel = self.bot.config.channels.bm

    @commands.command(aliases=["bM", "bm"])
    async def bM_meter(self, ctx, *, parameter: Optional[str]):
        """decides Based or Cringe"""
        # filter and truncate parameter
        parameter = parameter.replace("```", "Armenium") if parameter else "Your"
        parameter = parameter[:1000] + (parameter[250:] and "[…]")
        # set seed so that bot decides consistently
        random.seed(self.bot.static.remove_strange_chars(parameter.lower()))
        # decide if based or cringe
        bc_decision = random.choice(["Based", "Cringe"])
        punctuation_ending = random.choice(["!", "."]) * random.randint(1, 8)
        # send response
        await ctx.send(f"**{parameter}** are **{bc_decision}**{punctuation_ending}")
        # truncate response again
        parameter = parameter[:250] + (parameter[250:] and "[…]")
        # log response if not already logged
        if parameter in self.logged:
            return
        await self.bm_channel.send(f"```\n{parameter}, {bc_decision}{punctuation_ending}\n```")
        async with open("configs/randomized.json", "w") as file:
            self.logged.append(parameter)
            json.dump(self.logged, file)



    @commands.command(aliases=["gm", "gobi"])
    async def gobi_meter(self, ctx, *, phrase: str):
        random.seed(self.bot.static.remove_strange_chars(phrase.lower()))
        percent = round(random.random() * 100, 1)
        await ctx.channel.send(f"\"{phrase}\" is {percent}% Gobi")

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
