from typing import Optional
import random
import re

from discord.ext import commands

from utils.classes import RatBot
from utils.functions import safe_dump, safe_load, strip_str
from utils.random_band import BandRetrieval


class Randomized(commands.Cog):
    def __init__(self, bot: RatBot):
        self.bot = bot
        self.bands = BandRetrieval()
        self.bmed: list[str] = safe_load("data/bm.json", [])
        self.songs: dict[str, str] = safe_load("data/songs.json", {})
        self.bot.data.songs = list(self.songs.keys())

    @commands.command(aliases=["rb", "bands"])
    @commands.cooldown(2, 45, commands.BucketType.guild)
    @commands.max_concurrency(1, commands.BucketType.user)
    async def random_bands(
        self, ctx: commands.Context, upper_limit: int = 3, sort_method: str = "band", *, _filter: str = ""
    ):
        """Return x amount of bands from metal-archives.com
        If set, the amount of bands must between 1 to 10"""
        if not (1 <= upper_limit <= 10 or ctx.author.id == self.bot.owner_id):
            raise commands.BadArgument('Parameter "integer" must range from 1 to 10.')

        bands = await self.bands.format(
            str(ctx.author.id), upper_limit, sort_method, _filter=_filter, iteration_hard_limit=(upper_limit * 10)
        )
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
    async def based_meter(self, ctx: commands.Context, *, argument: Optional[str]):
        """Determines basedness of an argument"""
        if isinstance(argument, str):
            argument = argument[:1000] + (" [...]" if argument[1000:] else "")
            argument = argument.replace("*", "").replace("`", "")
        if not argument:
            raise commands.BadArgument("**Your are Cringe!!!!!!!!!**")

        determination = random.choice(["Based", "Cringe"])
        emphasis = random.choice(["!", ".", "?"]) * random.randint(1, 8)

        await ctx.send(f"**{argument}** are **{determination}{emphasis}**")
        if argument not in self.bmed:
            await self.bot.status_channels.BM.send(f"```{argument}, {determination}{emphasis}```")
            self.bmed.append(argument)
            safe_dump("data/bm.json", self.bmed)

    @commands.command(aliases=["gobi"])
    async def gobi_percentage(self, ctx: commands.Context, *, argument: Optional[str]):
        """Determines gobiness of an argument"""
        if isinstance(argument, str):
            argument = argument[:1000] + (" [...]" if argument[1000:] else "")
        if not argument:
            raise commands.BadArgument("**Your are 100% Gobi.**")

        seed = strip_str(argument)
        random.seed(seed)

        determination = round(random.random() * 100, 2)
        await ctx.send(f"{argument} are {determination}% Gobi.")

    @commands.command(aliases=["hex", "rcolor", "rc"])
    async def random_hexadecimal_color(self, ctx: commands.Context):
        """Returns a randomized hexadecimal color"""
        await ctx.send("`#" + ("%06x" % random.randint(0, 0xFFFFFF)) + "`")

    @commands.command(aliases=["choice", "choose"])
    async def pick(self, ctx: commands.Context, *arguments: str):
        """
        Chooses one random item split by spaces

        Multiple word items can be split with quotation blocks: 'r.choose item1 "item 2" item3'
        """
        await ctx.send("`" + random.choice(arguments).replace("`", r"\`") + "`")

    @commands.group(aliases=["song", "rs"], invoke_without_command=True)
    async def random_song(self, ctx: commands.Context):
        """Returns a random song from a saved directory"""
        if not self.bot.data.songs:
            raise commands.CommandError("Bot does not have any songs")
        await ctx.send("https://youtu.be/" + random.choice(self.bot.data.songs))

    @random_song.command()
    @commands.is_owner()
    async def update(self, ctx: commands.Context, link: str, *, title: str):
        link = re.sub(r"(https?:\/\/)?(www.)?(youtube.com|youtu.be)\/(watch\?v=)?", "", link)
        link = re.sub(r"&.+=.+$", "", link)

        if link in self.bot.data.songs:
            await ctx.send(f"Overwriting `{link}`: `{self.songs[link]}`")
        self.songs[link] = title
        safe_dump("data/songs.json", self.songs)
        self.bot.data.songs = list(self.songs.keys())
        await ctx.send(f"Set `{link}` to `{title}`")

    @random_song.command()
    @commands.is_owner()
    async def list(self, ctx: commands.Context):
        resp = "```\n"
        resp += "self.songs:\n   " + "\n   ".join(str(item) for item in self.songs.items()).strip()
        resp += "\n```"
        await ctx.send(resp)


def setup(bot: RatBot):
    bot.add_cog(Randomized(bot))
