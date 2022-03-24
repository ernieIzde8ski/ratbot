from random import randint
from typing import Optional, Union

from aiohttp import ClientSession
from discord import Color, Embed
from discord.ext import commands, tasks
from fuzzywuzzy import fuzz
from utils import RatBot, RatCog, safe_dump, safe_load


class XKCD(RatCog):
    """Interactions with XKCD comics"""

    # TODO: Rewrite

    def __init__(self, bot: RatBot):
        super().__init__(bot=bot)
        self.xkcds = safe_load("data/xkcd.json", [{"int": -1}])
        self.update_index.start()

    async def get_best_match(self, string) -> int:
        xkcds = sorted(self.xkcds, key=lambda xkcd: fuzz.ratio(xkcd["name"].lower(), string), reverse=True)
        return xkcds[0]["int"]

    @staticmethod
    def embed_constructor(xkcd: dict) -> Embed:
        return (
            Embed(title=f"{xkcd['num']}: {xkcd['title']}", url=f"https://xkcd.com/{xkcd['num']}", color=Color.random())
            .set_image(url=xkcd["img"])
            .set_footer(text=xkcd["alt"])
        )

    @staticmethod
    async def get_xkcd(id: int) -> dict:
        if id == -1:
            url = "https://xkcd.com/info.0.json"
        else:
            url = f"https://xkcd.com/{id}/info.0.json"

        async with ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 404:
                    return {"error": "Invalid xkcd id"}
                return await resp.json()

    @commands.group(invoke_without_command=True, aliases=["x"])
    async def xkcd(self, ctx: commands.Context, *, argument: Optional[Union[int, str]]):
        """Return an XKCD from an argument"""
        if not argument:
            argument = -1
        elif isinstance(argument, str):
            argument = await self.get_best_match(argument.lower())

        xkcd = await self.get_xkcd(argument)
        if xkcd.get("error"):
            raise commands.BadArgument(xkcd["error"])
        embed = self.embed_constructor(xkcd)
        await ctx.send(embed=embed)

    @xkcd.command(aliases=["r"])
    async def random(self, ctx: commands.Context):
        """Returns a random XKCD"""
        id = randint(0, self._latest["num"])

        xkcd = await self.get_xkcd(id)
        if xkcd.get("error"):
            raise commands.BadArgument(xkcd["error"])

        embed = self.embed_constructor(xkcd)
        await ctx.send(embed=embed)

    @xkcd.command(aliases=["l"])
    async def latest(self, ctx: commands.Context):
        """Returns the latest XKCD"""
        xkcd = await self.get_xkcd(-1)
        if xkcd.get("error"):
            raise commands.BadArgument(xkcd["error"])

        embed = self.embed_constructor(xkcd)
        await ctx.send(embed=embed)

        if xkcd["num"] != self._latest["num"]:
            self.update_index.cancel()
            self.update_index.start()

    @tasks.loop(hours=6)
    async def update_index(self):
        self._latest = await self.get_xkcd(-1)
        if self._latest.get("error"):
            return
        if self._latest["num"] <= self.xkcds[-1]["int"]:
            print("No new XKCDs")
            return
        for i in range(self.xkcds[-1]["int"] + 1, self._latest["num"] + 1):
            xkcd = await self.get_xkcd(i)
            if xkcd.get("error"):
                continue
            self.xkcds.append({"name": xkcd["title"], "alt": xkcd["alt"], "int": xkcd["num"]})
        safe_dump("data/xkcd.json", self.xkcds)
        print("Updated XKCDs")


def setup(bot: RatBot):
    bot.add_cog(XKCD(bot))
