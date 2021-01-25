# this seems to like to generate a weird error a lot of the time:
#   C:\Users\izdeb\AppData\Local\Programs\Python\Python39\lib\site-packages\hypixelaPY\objects\stats.py:57: RuntimeWarning: coroutine 'get_api_stats' was never awaited
#     self.ratio = Ratio(self.kills, self.deaths)
# it might be fixed now in the latest hypixelaPY ?
import discord
import discord.ext.commands as commands
import asyncio
from hypixelaPY import Hypixel

from token import api_key
hypixel = Hypixel(api_key)

class hypixelbasedlevels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bm_hypixel(self, ctx, player_name):
        player = await hypixel.player.get(name=player_name)
        await ctx.send("based") if player.bedwars.games_played < 10 else await ctx.send(f"cringe ({player.bedwars.games_played} Cringegamecount)")

def setup(bot):
    bot.add_cog(hypixelbasedlevels(bot))
