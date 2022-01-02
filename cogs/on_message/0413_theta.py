import discord
from discord.ext import commands
from fuzzywuzzy import fuzz
from utils.classes import RatBot
from utils.functions import safe_dump, safe_load


class AEBDTheta(commands.Cog):
    """Handle processes related to 0413-Theta (primary_guild in config)"""

    def __init__(self, bot: RatBot):
        self.bot = bot
        self.armenium_facts: int = safe_load("data/facts.json", 0)
        self.bot.loop.create_task(self.set_channel())

    async def set_channel(self):
        await self.bot.wait_until_ready()
        self.channel: discord.TextChannel = self.bot.get_channel(884237172717277225)

    @commands.command()
    @commands.is_owner()
    async def set_facts(self, ctx: commands.Context, arg: int):
        """Set total Armenium Facts"""
        self.armenium_facts = arg
        await self.channel.edit(topic=f"**Armenium** is intimidated by **Men**.\nKnown **Armenium** Facts: {self.armenium_facts}")
        safe_dump("data/facts.json", self.armenium_facts)
        await ctx.send(f"Set armenium facts to `{self.armenium_facts}`")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == 304118384663068673 and message.channel.id == self.channel.id:
            if fuzz.ratio(message.content.lower(), "**daily 'armenium' fact**") > 85:
                return
            self.armenium_facts += 1
            await self.channel.edit(topic=f"**Armenium** is intimidated by **Men**.\nKnown **Armenium** Facts: {self.armenium_facts}")


def setup(bot: RatBot) -> None:
    bot.add_cog(AEBDTheta(bot))
