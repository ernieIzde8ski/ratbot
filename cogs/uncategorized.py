from random import choice

from discord import Embed, Permissions, utils
from discord.ext import commands


class Uncategorized(commands.Cog):
    """There is only one command here Doe?
    Yea"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["support", "info", "invite"])
    async def information(self, ctx):
        """Provides general/support information"""
        bot_owner = (await commands.Bot.application_info(self.bot)).owner
        embed = Embed(
            name="Awesome?",
            description=f"[GitHub](https://github.com/ernieIzde8ski/ratbot)\n"
                        f"[Bot Invite]({utils.oauth_url(self.bot.id, permissions=Permissions(8))})\n"
                        f"[bot invite but you have to think about it]({utils.oauth_url(self.bot.id, permissions=Permissions(201714752))}\n"
                        f"[\"Support Server\"](https://discord.gg/cHZYahK)\n"
                        f"[Good song](https://www.youtube.com/watch?v={choice(ctx.bot.config.songs)})",
            color=ctx.author.color, timestamp=ctx.message.created_at
        ).set_author(name=bot_owner, icon_url=bot_owner.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Uncategorized(bot))
