from typing import Union

import discord.ext.commands as commands
from aiohttp import ClientSession
from discord import Embed


class XKCD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def get_xkcd(xkcd_id: Union[int, None]):
        async with ClientSession() as session:
            async with session.get("http://xkcd.com{}info.0.json".format(f"/{xkcd_id}/" if xkcd_id else "/")) as resp:
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
    async def xkcd(self, ctx, *, xkcd_id: Union[int, str, None]):
        if isinstance(xkcd_id, int):
            xkcd_json = await self.get_xkcd(xkcd_id)
            embed = await self.embed_constructor(xkcd_json, ctx.author.color)
            await ctx.channel.send(embed=embed)
        elif isinstance(xkcd_id, str):
            await ctx.send(f"Sorry I Don't know how to handle looking for `{xkcd_id}` ( Yet)")
        else:
            await ctx.send("Please provide Input")

    @xkcd.command()
    async def latest(self, ctx):
        xkcd_json = await self.get_xkcd(xkcd_id=None)
        embed = await self.embed_constructor(xkcd_json, ctx.author.color)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(XKCD(bot))
