import discord.ext.commands as commands
from hypixelaPY import exceptions


class HypixelBasedLevels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["bmh"])
    async def bm_hypixel(self, ctx, player_name):
        """Determines whether a person is based or cringe, judging by their total plays in bedwars"""
        try:
            player = await self.bot.hypixel.player.get(name=player_name)
        except exceptions.NoPlayerFoundError:
            await ctx.send("that Does not seem to be a Real Player")
        else:
            await ctx.send(
                "based" if player.bedwars.games_played < 10 else f"cringe ({player.bedwars.games_played} Cringegamecount)"
            )


def setup(bot):
    bot.add_cog(HypixelBasedLevels(bot))
