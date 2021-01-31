import discord
from discord.ext import commands


from random import choice
from config import songs


class Uncategorized(commands.Cog):
    """There is only one command here Doe?"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["support", "info"])
    async def information(self, ctx):
        """Provides general/support information"""
        bot_owner = (await commands.Bot.application_info(self.bot)).owner
        embed = discord.Embed(
        name="Awesome?",
        description=f"[GitHub](https://github.com/ernieIzde8ski/ratbot)\n"
            f"[Bot Invite](https://discordapp.com/api/oauth2/authorize?client_id=466737001832382464&permissions=8&scope=bot)\n"
            f"[\"Support Server\"](https://discord.gg/cHZYahK)\n"
            f"[Good song](https://www.youtube.com/watch?v={choice(songs)})",
            color=ctx.author.color, timestamp=ctx.message.created_at
        ).set_author(name=bot_owner, icon_url=bot_owner.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Uncategorized(bot))
