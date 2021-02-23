# Error Gone I Ran 1.2.0 Instead Of 1.2.5

import discord.ext.commands as commands


class HypixelBasedLevels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bm_hypixel(self, ctx, player_name):
        """Determines whether a person is based or cringe, judging by their total plays in bedwars"""
        player = await self.bot.hypixel.player.get(name=player_name)
        await ctx.send(
            "based" if player.bedwars.games_played < 10 else f"cringe ({player.bedwars.games_played} Cringegamecount)")


def setup(bot):
    bot.add_cog(HypixelBasedLevels(bot))
