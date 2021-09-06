import discord
from discord.ext import commands
from fuzzywuzzy import fuzz
from modules._json import safe_load, safe_dump


class AEBDTheta(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.armenium_facts: int = safe_load("data/facts.json", 0)
        self.channel: discord.TextChannel = self.bot.get_channel(
            884237172717277225)

    @commands.command()
    @commands.is_owner()
    async def set_facts(self, ctx: commands.Context, arg: int):
        await self.channel.edit(topic=f"**Armenium is intimidated by **Men**.\nKnown Armenium Facts: {self.armenium_facts := self.armenium_facts + 1}")
        safe_dump("data/facts.json", self.armenium_facts)
        await ctx.send(f"Set armenium facts to `{self.armenium_facts}`")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == 304118384663068673 and message.channel.id == self.channel.id:
            if fuzz.ratio(message.content.lower(), "**daily 'armenium' fact**") > 85:
                return
            await self.channel.edit(topic=f"**Armenium is intimidated by **Men**.\nKnown Armenium Facts: {self.armenium_facts := self.armenium_facts + 1}")


def setup(bot: commands.Bot) -> None:
    bot.add_cog(AEBDTheta(bot))
