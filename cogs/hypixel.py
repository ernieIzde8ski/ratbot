# this seems to like to generate a weird error a lot of the time:
#   C:\Users\izdeb\AppData\Local\Programs\Python\Python39\lib\site-packages\hypixelaPY\objects\stats.py:57: RuntimeWarning: coroutine 'get_api_stats' was never awaited
#     self.ratio = Ratio(self.kills, self.deaths)
# it might be fixed now in the latest hypixelaPY ?
from secrets import api_key

import discord.ext.commands as commands
from hypixelaPY import Hypixel


class HypixelBasedLevels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.loop.create_task(self._initialize_hypixel())

    async def _initialize_hypixel(self):
        self.hypixel = await Hypixel(api_key)

    @commands.command()
    async def bm_hypixel(self, ctx, player_name):
        player = await self.hypixel.player.get(name=player_name)
        await ctx.send("based") if player.bedwars.games_played < 10 else await ctx.send(
            f"cringe ({player.bedwars.games_played} Cringegamecount)")


def setup(bot):
    bot.add_cog(HypixelBasedLevels(bot))
