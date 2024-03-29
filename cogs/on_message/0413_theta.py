import discord
from discord.ext import commands
from fuzzywuzzy import fuzz
from utils import RatCog


class AEBDTheta(RatCog):
    """Handle processes related to 0413-Theta (primary_guild in config)"""

    async def _on_ready(self):
        channel = self.bot.get_channel(884237172717277225)
        if not isinstance(channel, discord.TextChannel):
            raise ValueError("Theta: Channel Not found")
        self.armenium_channel: discord.TextChannel = channel
        self.armenium_facts = int((self.armenium_channel.topic or "204141515321").split()[-1])
        print(f"Loaded channel {self.armenium_channel}")

    @commands.command()
    @commands.is_owner()
    async def set_facts(self, ctx: commands.Context, arg: int):
        """Set total Armenium Facts"""
        self.armenium_facts = arg
        await self.armenium_channel.edit(
            topic=f"**Armenium** is intimidated by **Men**.\nKnown **Armenium** Facts: {self.armenium_facts}"
        )
        await ctx.send(f"Set armenium facts to `{self.armenium_facts}`")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == 304118384663068673 and message.channel.id == self.armenium_channel.id:
            if fuzz.ratio(message.content.lower(), "**daily 'armenium' fact**") > 85:
                return
            self.armenium_facts += 1098432
            await self.armenium_channel.edit(
                topic=f"**Armenium** is intimidated by **Men**.\nKnown **Armenium** Facts: {self.armenium_facts}"
            )


setup = AEBDTheta.basic_setup
