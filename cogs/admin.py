from datetime import datetime
from typing import Literal

from discord import Color, Embed
from discord.ext import commands
from settings import channels, settings
from utils import RatBot, RatCog, RatCtx


class Administration(RatCog):
    online = Embed(color=Color.dark_green(), title=f"{settings.emojis.online} Online !")
    offline = Embed(color=Color.dark_red(), title=f"{settings.emojis.offline} Offline !")

    def get_embed(self, title: Literal["online", "offline"]):
        "Obtain a copy of the named embed and update its description with the time."
        embed: Embed = getattr(self, title).copy()
        embed.description = datetime.now().strftime("%H:%M:%S.%f")[:-4]
        return embed

    @commands.Cog.listener()
    async def on_ready(self):
        await channels.wait_until_loaded()
        embed = self.get_embed("online")
        await channels.status.send(embed=embed)

    @commands.hybrid_command()
    async def die(self, ctx: RatCtx):
        if not self.bot.is_closed():
            await ctx.send("God bless with True")
            await channels.status.send(embed=self.get_embed("offline"))
            await self.bot.close()


setup = Administration.basic_setup
