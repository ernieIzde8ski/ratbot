import random
import re
from discord.ext import commands
from typing import Optional, Union

from modules._json import safe_load, safe_dump
from modules.functions import reduce
from modules.random_band import format


class Randomized(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bmed = safe_load("data/bm.json", [])
        self.songs = safe_load("data/songs.json", {})
        self.bot.songs = list(self.songs.keys())

    @commands.command(aliases=["rb", "bands"])
    @commands.cooldown(1, 45, commands.BucketType.user)
    @commands.cooldown(1, 15, commands.BucketType.guild)
    async def random_bands(self, ctx, integer: int = 3):
        """Return x amount of bands from metal-archives.com
        If set, the amount of bands must between 1 to 10"""
        if not (1 <= integer <= 10 or ctx.author.id == self.bot.owner_id):
            print(ctx.author.id)
            print(self.bot.owner_id)
            return await ctx.send(f"{integer} is an invalid amount of bands (range from 1 to 10)")

        bands = await format(integer)
        await ctx.send(f"```\n{bands}\n```")

    @commands.command(aliases=["bm"])
    async def based_meter(self, ctx, *, argument: Optional[str]):
        """Determines basedness of an argument"""
        if isinstance(argument, str):
            argument = argument[:1000] + (" [...]" if argument[1000:] else "")
            argument = argument.replace("*", "").replace("`", "")
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
        """Determines gobiness of an argument"""
        if isinstance(argument, str):
            argument = argument[:1000] + (" [...]" if argument[1000:] else "")
        if not argument:
            return await ctx.send("**Your are 100% Gobi.**")

        seed = reduce(argument)
        random.seed(seed)

        determination = round(random.random() * 100, 2)
        await ctx.send(f"{argument} are {determination}% Gobi.")
    
    @commands.command(aliases=["choose"])
    async def choice(self, ctx, *, arguments: str):
        arguments = [argument for argument in re.split(r",\s*", arguments) if argument]
        if not arguments:
            return await ctx.send("Arguments are required")
        await ctx.send("`" + random.choice(arguments).replace("`", "") + "`")

    @commands.group(aliases=["song"], invoke_without_command=True)
    async def random_song(self, ctx):
        """Returns a random song from a saved directory"""
        if not self.bot.songs:
            return await ctx.send("There are no songs Lol")
        await ctx.send("https://youtu.be/" + random.choice(self.bot.songs))

    @random_song.command()
    @commands.is_owner()
    async def update(self, ctx, link: str, *, title: str):
        link = re.sub(r"&.+=.+$", "", link)
        link = link.removeprefix("https://youtu.be/").removeprefix("https://www.youtube.com/watch?v=")

        if link in self.bot.songs:
            await ctx.send(f"Overwriting `{link}`: `{self.songs[link]}`")
        self.songs[link] = title
        safe_dump("data/songs.json", self.songs)
        self.bot.songs = list(self.songs.keys())
        await ctx.send(f"Set {link} to {title}")


def setup(bot):
    bot.add_cog(Randomized(bot))
