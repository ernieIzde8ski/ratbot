from typing import Union

from discord.ext import commands


class XKCD(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def xkcd(self, ctx, *, xkcd_id: Union[int, str, None]):
        idtype = xkcd_id.__class__.__name__
        if idtype == "int":
            return await ctx.channel.send(f"https://xkcd.com/{xkcd_id}/")
        elif idtype == "str":
            await ctx.send(f"Sorry I Don't know how to handle looking for {xkcd_id} ( Yet)")
        else:
            await ctx.send("Please provide Input")


def setup(bot):
    bot.add_cog(XKCD(bot))
