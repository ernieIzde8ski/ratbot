from discord.ext import commands
from discord import Embed, Color, Permissions, utils
from random import choice


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["info", "support"])
    async def information(self, ctx: commands.Context):
        main = f"[GitHub]({self.bot.config['github']})\n" \
               f"[Bot Invite]({utils.oauth_url(self.bot.user.id, permissions=Permissions(2214915137))})\n" \
               f"[Server Invite]({self.bot.config['invite']})\n" \
               f"[Random Song](https://youtu.be/{choice(self.bot.songs)})"
        footer = f"Commands can be invoked with the prefix(es) " \
                 f"(default: {' || '.join(self.bot.config['prefix'])}`) " \
                 f"or with a mention (@{ctx.me})"

        embed = Embed(
            title="Information, Support",
            description=main,
            color=ctx.me.color
        ).set_footer(text=footer, icon_url=self.bot.app.owner.avatar_url)

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
