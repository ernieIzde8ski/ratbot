from typing import Optional
import random
import re

from discord.ext import commands
from discord import Embed

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
    @commands.cooldown(2, 45, commands.BucketType.guild)
    async def random_bands(self, ctx, integer: int = 3, sort_method: str = "band"):
        """Return x amount of bands from metal-archives.com
        If set, the amount of bands must between 1 to 10"""
        if not (1 <= integer <= 10 or ctx.author.id == self.bot.owner_id):
            raise commands.BadArgument("Parameter \"integer\" must range from 1 to 10.")

        bands = await format(integer, sort_method)
        await self.split_message(ctx, bands)

    @staticmethod
    async def split_message(ctx: commands.Context, message: str) -> None:
        """Takes a long message and splits it into multiple, surrounded by code blocks"""
        if message.__len__() < 1950:
            await ctx.send(f"```\n{message}\n```")
            return

        lines = message.split("\n")
        resp = ""
        for line in lines:
            if (line.__len__() + resp.__len__() < 1950) and (line != lines[-1]):
                resp += f"\n{line}"
            else:
                await ctx.send(f"```\n{resp}\n```")
                resp = line

    @commands.command(aliases=["bm"])
    async def based_meter(self, ctx, *, argument: Optional[str]):
        """Determines basedness of an argument"""
        if isinstance(argument, str):
            argument = argument[:1000] + (" [...]" if argument[1000:] else "")
            argument = argument.replace("*", "").replace("`", "")
        if not argument:
            raise commands.BadArgument("**Your are Cringe!!!!!!!!!**")

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
            raise commands.BadArgument("**Your are 100% Gobi.**")

        seed = reduce(argument)
        random.seed(seed)

        determination = round(random.random() * 100, 2)
        await ctx.send(f"{argument} are {determination}% Gobi.")

    @commands.command(aliases=["choose"])
    async def choice(self, ctx, *, arguments: str):
        arguments = [argument for argument in re.split(
            r",\s*", arguments) if argument]
        if not arguments.__len__():
            raise commands.ArgumentParsingError(
                "arguments is a required argument that is missing.")
        await ctx.send("`" + random.choice(arguments).replace("`", "") + "`")

    @commands.group(aliases=["song", "rs"], invoke_without_command=True)
    async def random_song(self, ctx):
        """Returns a random song from a saved directory"""
        if not self.bot.songs:
            raise commands.CommandError("Bot does not have any songs")
        await ctx.send("https://youtu.be/" + random.choice(self.bot.songs))

    @random_song.command()
    @commands.is_owner()
    async def update(self, ctx, link: str, *, title: str):
        link = re.sub(
            r"(https?:\/\/)?(www.)?(youtube.com|youtu.be)\/(watch\?v=)?", "", link)
        link = re.sub(r"&.+=.+$", "", link)

        if link in self.bot.songs:
            await ctx.send(f"Overwriting `{link}`: `{self.songs[link]}`")
        self.songs[link] = title
        safe_dump("data/songs.json", self.songs)
        self.bot.songs = list(self.songs.keys())
        await ctx.send(f"Set {link} to {title}")

    @random_song.command()
    @commands.is_owner()
    async def list(self, ctx):
        resp = "```\nself.bot.songs:\n   " + \
            "\n   ".join(self.bot.songs).strip()
        items = [str(item) for item in self.songs.items()]
        resp += "\nself.songs:\n   " + "\n   ".join(items).strip()
        resp += "\n```"
        await ctx.send(resp)


def setup(bot):
    bot.add_cog(Randomized(bot))
