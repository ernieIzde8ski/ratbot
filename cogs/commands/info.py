from random import choice

from discord import Embed, Permissions, utils
from discord.ext import commands
from utils import RatCog

PERMISSIONS = Permissions(2214915137)


class Information(RatCog):
    """A single informatic command pertaining to RatBot"""

    async def _on_ready(self) -> None:
        assert self.bot.user
        self.invite = utils.oauth_url(self.bot.user.id, permissions=PERMISSIONS)
        self.prefixes = " || ".join(self.bot.config.prefix)

    @commands.command(aliases=["info", "support"])
    async def information(self, ctx: commands.Context):
        """Provide useful information"""
        main = (
            f"[Server Invite]({self.bot.config.invite})\n"
            f"[GitHub]({self.bot.config.github})\n"
            f"[Bot Invite]({self.invite})\n"
            f"[Random Song](https://youtu.be/{choice(list(self.bot.settings.songs))})"
        )
        footer = (
            f"Commands can be invoked with the prefix(es) "
            f"(default: {self.prefixes}`) "
            f"or with a mention (@{ctx.me})"
        )

        embed = Embed(title="Information, Support", description=main, color=ctx.me.color).set_footer(
            text=footer, icon_url=self.bot.app.owner.avatar.url if self.bot.app.owner.avatar else None
        )

        await ctx.send(embed=embed)


setup = Information.basic_setup
