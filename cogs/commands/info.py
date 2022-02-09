from random import choice

from discord import Embed, Permissions, utils
from discord.ext import commands
from bot import RatBot

PERMISSIONS = Permissions(2214915137)


class Information(commands.Cog):
    def __init__(self, bot: RatBot):
        self.bot = bot
        self.bot.loop.create_task(self.initialize())

    async def initialize(self) -> None:
        await self.bot.wait_until_ready()
        self.invite = utils.oauth_url(self.bot.user.id, permissions=PERMISSIONS)
        self.prefixes = " || ".join(self.bot.config["prefix"])

    @commands.command(aliases=["info", "support"])
    async def information(self, ctx: commands.Context):
        """Provide useful information"""
        main = (
            f"[Server Invite]({self.bot.config['invite']})\n"
            f"[GitHub]({self.bot.config['github']})\n"
            f"[Bot Invite]({self.invite})\n"
            f"[Random Song](https://youtu.be/{choice(self.bot.data.songs)})"
        )
        footer = (
            f"Commands can be invoked with the prefix(es) "
            f"(default: {self.prefixes}`) "
            f"or with a mention (@{ctx.me})"
        )

        embed = Embed(title="Information, Support", description=main, color=ctx.me.color).set_footer(
            text=footer, icon_url=self.bot.app.owner.avatar_url
        )

        await ctx.send(embed=embed)


def setup(bot: RatBot):
    bot.add_cog(Information(bot))
