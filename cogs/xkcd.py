from random import randint
from typing import Union

import discord.ext.commands as commands
from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError
from discord import Embed


class XKCD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def get_xkcd(xkcd_id: Union[int, None]) -> dict:
        async with ClientSession() as session:
            async with session.get("https://xkcd.com{}info.0.json".format(f"/{xkcd_id}/" if xkcd_id else "/")) as resp:
                return await resp.json()

    @staticmethod
    async def embed_constructor(data, color) -> Embed:
        return Embed(
            title=f"{data['num']}: {data['title']}",
            url=f"https://xkcd.com/{data['num']}/",
            color=color
        ).set_footer(
            text=data['alt']
        ).set_image(
            url=data['img']
        )

    async def get_random_xkcd(self) -> dict:
        latest_xkcd = (await self.get_xkcd(None))['num']
        while True:
            num = randint(1, latest_xkcd)
            if num != 404: break
        return await self.get_xkcd(num)

    @commands.group(invoke_without_command=True)
    async def xkcd(self, ctx, *, xkcd_id: Union[int, str] = 221):
        """get xkcd command from id"""
        if isinstance(xkcd_id, int):
            try:
                xkcd_json = await self.get_xkcd(xkcd_id)
            except ContentTypeError as e:
                await ctx.send(f"`ContentTypeError: {e}`")
                await ctx.send(f"was your input valid?")
                return
            embed = await self.embed_constructor(xkcd_json, ctx.author.color)
            await ctx.send(embed=embed)
        elif isinstance(xkcd_id, str):
            await ctx.send(f"Sorry I Don't know how to handle string lookup ( Yet)")

    @xkcd.command()
    async def latest(self, ctx):
        """get the latest xkcd"""
        xkcd_json = await self.get_xkcd(xkcd_id=None)
        embed = await self.embed_constructor(xkcd_json, ctx.author.color)
        await ctx.send(embed=embed)

    @xkcd.command()
    async def random(self, ctx):
        """get random xkcd"""
        xkcd_dict = await self.get_random_xkcd()
        embed = await self.embed_constructor(xkcd_dict, ctx.author.color)
        await ctx.send(embed=embed)

    @xkcd.group(invoke_without_command=True)
    async def explain(self, ctx, *, xkcd_id: Union[int, str] = 221):
        """links to an xkcd explanation"""
        try:
            data = await self.get_xkcd(xkcd_id)
        except ContentTypeError as e:
            await ctx.send(f"`ContentTypeError: {e}`")
            await ctx.send(f"was your input valid?")
            return
        link = f"https://explainxkcd.com/{data['num']}"
        await ctx.send(link)

    @explain.command()
    async def latest(self, ctx):
        """links to the latest xkcd explanation"""
        data = await self.get_xkcd(xkcd_id=None)
        link = f"https://explainxkcd.com/{data['num']}"
        await ctx.send(link)

    @explain.command()
    async def random(self, ctx):
        """links to random xkcd explanation"""
        data = await self.get_random_xkcd()
        link = f"https://explainxkcd.com/{data['num']}"
        await ctx.send(link)


def setup(bot):
    bot.add_cog(XKCD(bot))
