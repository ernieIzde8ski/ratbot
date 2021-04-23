from typing import Union

import discord.ext.commands as commands
from aiohttp import ClientSession
from aiohttp.client_exceptions import ContentTypeError
from discord import Embed
from random import randint


class XKCD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def get_xkcd(xkcd_id: Union[int, None]):
        async with ClientSession() as session:
            async with session.get("https://xkcd.com{}info.0.json".format(f"/{xkcd_id}/" if xkcd_id else "/")) as resp:
                return await resp.json()

    @staticmethod
    async def embed_constructor(data, color):
        return Embed(
            title=data['title'],
            url=f"https://xkcd.com/{data['num']}/",
            color=color
        ).set_footer(
            text=data['alt']
        ).set_image(
            url=data['img']
        )

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
        latest_xkcd = (await self.get_xkcd(None))['num']
        while True:
            num = randint(1, latest_xkcd)
            if num != 404: break
        xkcd_json = await self.get_xkcd(num)
        embed = await self.embed_constructor(xkcd_json, ctx.author.color)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(XKCD(bot))
