from random import choice

import discord.ext.commands as commands
from discord import Embed, Permissions, utils


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def embed_constructor(self, ctx):
        bot_owner = (await commands.Bot.application_info(self.bot)).owner
        return Embed(
            name="Lol?", color=ctx.author.color,
            description=f"[GitHub](https://github.com/ernieIzde8ski/ratbot)\n"
                        f"[Invitame]({utils.oauth_url(self.bot.user.id, permissions=Permissions(8))})\n"
                        f"[invitación pero necesitas pensar]({utils.oauth_url(self.bot.user.id, permissions=Permissions(201714752))})\n"
                        f"[\"Support Server\"](https://discord.gg/cHZYahK)\n"
                        f"[Good song](https://www.youtube.com/watch?v={choice(self.bot.config.songs)})",
        ).set_author(
            name=f"— {bot_owner}",
            icon_url=bot_owner.avatar_url
        ).set_footer(
            text="Default Prefix Is {} If You Haven't Figured That Out Lol".format(
                self.bot.config.prefix[0] if isinstance(self.bot.config.prefix, tuple) else self.bot.config.prefix
            )
        )

    @commands.command(aliases=["support", "ayuda", "eyy"])
    async def info(self, ctx):
        embed = await self.embed_constructor(ctx)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
