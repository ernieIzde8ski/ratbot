import discord.ext.commands as commands
from aiohttp import ClientSession

from configs.secrets import tenor_api_key as apikey


class Tenor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def get_tenor(query) -> str:
        async with ClientSession() as session:
            async with session.get(f"https://g.tenor.com/v1/search?q={query}&key={apikey}&limit=1") as resp:
                json = await resp.json()
                return json['results'][0]['url']

    @commands.command(aliases=["t"])
    async def tenor(self, ctx, *, query):
        await ctx.send(await self.get_tenor(query))


def setup(bot):
    bot.add_cog(Tenor(bot))
