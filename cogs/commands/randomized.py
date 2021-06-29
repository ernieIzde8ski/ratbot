from typing import Optional
from modules._json import safe_load, safe_dump
from modules.functions import reduce
import modules.random_band as rb
from discord.ext import commands
import random


class Randomized(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bmed = safe_load("data/bm.json", [])

    @commands.command(aliases=["rb", "bands"])
    @commands.cooldown(1, 45, commands.BucketType.user)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def random_bands(self, ctx, integer: int = 3):
        if not (1 <= integer <= 10):
            return await ctx.send(f"{integer} is an invalid amount of bands (range from 1 to 10)")

        bands = await rb.format(integer)
        await ctx.send(f"```{bands}```")

    @random_bands.error
    async def random_bands_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply("Lol , command is on Cooldown")

    @commands.command(aliases=["bm"])
    async def based_meter(self, ctx, *, argument: Optional[str]):
        if isinstance(argument, str):
            argument = argument[:1000].replace("*", "").replace("`", "") + (" [...]" if argument[1000:] else "")
        if not argument:
            return await ctx.send("**Your are Cringe!!!!!!!!!**")

        seed = reduce(argument)
        random.seed(seed)

        determination = random.choice(["Based", "Cringe"])
        emphasis = random.choice(["!", ".", "?"]) * random.randint(1, 8)

        await ctx.send(f"**{argument}** are **{determination}{emphasis}**")
        if argument not in self.bmed:
            await self.bot.c.BMs.send(f"```{argument}, {determination}{emphasis}```")
            self.bmed.append(argument)
            safe_dump("data/bm.json", self.bmed)

    @commands.command(aliases=["gobi"])
    async def gobi_percentage(self, ctx, *, argument: Optional[str]):
        if isinstance(argument, str):
            argument = argument[:1000].replace("*", "").replace("`", "") + (" [...]" if argument[1000:] else "")
        if not argument:
            return await ctx.send("**Your are 100% Gobi.**")

        seed = reduce(argument)
        random.seed(seed)

        determination = round(random.random() * 100, 2)
        await ctx.send(f"{argument} are {determination}% Gobi.")


def setup(bot):
    bot.add_cog(Randomized(bot))
