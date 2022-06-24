import random
import re
from typing import Optional

from discord.ext import commands
from utils import BandRetrieval, RatCog, strip_str


class Randomized(RatCog):
    # TODO: Rewrite into a dependency module
    async def _on_ready(self):
        self.bands = BandRetrieval()

    async def cog_unload(self):
        await self.bands.close()

    @staticmethod
    async def split_message(ctx: commands.Context, message: str) -> None:
        """Takes a long message and splits it into multiple, surrounded by code blocks"""
        if message.__len__() < 1950:
            await ctx.send(message)
            return

        lines = message.split("\n")
        resp = ""
        for line in lines:
            if (len(line) + len(resp) < 1950) and (line != lines[-1]):
                resp += f"\n{line}"
            else:
                await ctx.send(resp)
                resp = line

    @commands.group(invoke_without_command=True, aliases=["rb", "bands"])
    @commands.cooldown(rate=5, per=60, type=commands.BucketType.guild)
    @commands.max_concurrency(number=1, per=commands.BucketType.user)
    async def random_bands(
        self, ctx: commands.Context, upper_limit: int = 3, sort_method: str = "band", *, _filter: str = ""
    ):
        """Return x amount of bands from metal-archives.com
        If set, the amount of bands must between 1 to 10"""
        if not (1 <= upper_limit <= 10 or ctx.author.id == self.bot.owner_id):
            raise commands.BadArgument('Parameter "integer" must range from 1 to 10.')

        bands = await self.bands.format(str(ctx.author.id), upper_limit, sort_method, _filter=_filter)
        await self.split_message(ctx, f"```\n{bands}\n```")

    @random_bands.command(aliases=["urls", "links"])
    @commands.max_concurrency(number=1, per=commands.BucketType.user)
    async def URLs(self, ctx: commands.Context, max_bands: int = 3):
        if not (1 <= max_bands <= 10) and not self.bot.is_owner(ctx.author):
            raise commands.BadArgument('Parameter "integer" must range from 1 to 10.')

        bands = self.bands.get_bands(max_bands=max_bands, hash=ctx.author, max_iterations=max_bands * 10)
        bands = "\n".join(band["url"] for band in await bands)
        await self.split_message(ctx, bands)

    @commands.command(aliases=["bm"])
    async def based_meter(self, ctx: commands.Context, *, argument: Optional[str]):
        """Determines basedness of an argument"""
        if isinstance(argument, str):
            argument = argument[:1000] + (" [...]" if argument[1000:] else "")
            argument = argument.replace("*", "").replace("`", "")
        if not argument:
            raise commands.BadArgument("**Your are Cringe!!!!!!!!!**")

        random.seed(strip_str(argument))
        determination = random.choice(["Based", "Cringe"])
        emphasis = random.choice(["!", ".", "?"]) * random.randint(1, 8)

        await ctx.send(f"**{argument}** are **{determination}{emphasis}**")

        if argument not in self.bot.settings.measured:
            await self.bot.status_channels.BM.send(f"```{argument}, {determination}{emphasis}```")
            self.bot.settings.measured.add(argument)
            self.bot.settings.save()

    @commands.command(aliases=["gobi"])
    async def gobi_percentage(self, ctx: commands.Context, *, argument: Optional[str]):
        """Determines gobiness of an argument"""
        if isinstance(argument, str):
            argument = (argument[:1000] + (" [...]" if argument[1000:] else "")).strip()
        if not argument:
            raise commands.BadArgument(r"**Your are 100% Gobi.**")

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
        Chooses one random item from a list split by spaces

        Multiple word items can be split with quotation blocks: 'r.choose item1 "item 2" item3'
        """
        await ctx.send("`" + random.choice(arguments).replace("`", r"\`") + "`")

    @commands.group(aliases=["song", "rs"], invoke_without_command=True)
    async def random_song(self, ctx: commands.Context):
        """Returns a random song from a saved directory"""
        if not self.songs:
            raise commands.CommandError("Bot does not have any songs")
        await ctx.send(f"https://youtu.be/{random.choice(list(self.songs))}")

    @random_song.command()
    @commands.is_owner()
    async def update(self, ctx: commands.Context, link: str, *, title: str):
        link = re.sub(r"(https?:\/\/)?(www.)?(youtube.com|youtu.be)\/(watch\?v=)?", "", link)
        link = re.sub(r"&.+=.+$", "", link)

        if link in self.songs:
            await ctx.send(f"Overwriting `{link}`: `{self.songs[link]}`")
        self.songs[link] = title
        await ctx.send(f"Set `{link}` to `{title}`")

    @random_song.command()
    @commands.is_owner()
    async def list(self, ctx: commands.Context):
        resp = "```\n"
        resp += "self.songs:\n   " + "\n   ".join(str(item) for item in self.songs.items()).strip()
        resp += "\n```"
        await ctx.send(resp)


setup = Randomized.basic_setup
