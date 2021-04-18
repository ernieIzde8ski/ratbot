from typing import Union

import aiohttp
from discord import Embed
from discord.ext import commands


class XKCD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def get_xkcd(xkcd_id: int):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://xkcd.com/{xkcd_id}/info.0.json") as resp:
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

    @commands.command()
    async def xkcd(self, ctx, *, xkcd_id: Union[int, str, None]):
        if isinstance(xkcd_id, int):
            xkcd_json = await self.get_xkcd(xkcd_id)
            embed = await self.embed_constructor(xkcd_json, ctx.author.color)
            await ctx.channel.send(embed=embed)
        elif isinstance(xkcd_id, str):
            await ctx.send(f"Sorry I Don't know how to handle looking for `{xkcd_id}` ( Yet)")
        else:
            await ctx.send("Please provide Input")


def setup(bot):
    bot.add_cog(XKCD(bot))
