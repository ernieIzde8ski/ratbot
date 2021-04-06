from random import choice

from discord import Embed, Permissions, utils
from discord.ext import commands


class Uncategorized(commands.Cog):
    """There is only one command here Doe?
    Yea"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_subcommand=True)
    async def help(self, ctx):
        """Provides general/support information"""
        bot_owner = (await commands.Bot.application_info(self.bot)).owner
        embed = Embed(
            name="Awesome?",
            description=f"[GitHub](https://github.com/ernieIzde8ski/ratbot)\n"
                        f"[Invitame]({utils.oauth_url(self.bot.user.id, permissions=Permissions(8))})\n"
                        f"[invitación pero necesitas pensar]({utils.oauth_url(self.bot.user.id, permissions=Permissions(201714752))})\n"
                        f"[\"Support Server\"](https://discord.gg/cHZYahK)\n"
                        f"[Good song](https://www.youtube.com/watch?v={choice(ctx.bot.config.songs)})",
            color=ctx.author.color, timestamp=ctx.message.created_at
        ).set_author(
            name=bot_owner,
            icon_url=bot_owner.avatar_url
        ).set_footer(
            text="do `r.help command` for information on commands"
        )
        await ctx.send(embed=embed)
        return

    @help.command(aliases=["cmd", "cmds"])
    async def commands(self, ctx):
        await ctx.send(commands.HelpCommand)


def setup(bot):
    bot.remove_command("help") & print("Saying the Bye-Bye to Help Command")
    bot.add_cog(Uncategorized(bot))
