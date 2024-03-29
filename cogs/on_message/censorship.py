from contextlib import suppress
import re

from discord import AllowedMentions, Message, NotFound
from discord.ext import commands
from fuzzywuzzy import fuzz
from utils import RatBot, RatCog, strip_str


tenor_pattern = re.compile(r"https{0,1}:\/\/(www.)*tenor.com\/view\/([a-z]|-)+\d+")
allowed_mentions = AllowedMentions.all()


class Censorship(RatCog):
    """Allows me to delete things I don't like"""

    async def on_twitter(self, message: Message) -> None:
        if (
            not message.guild
            or message.author.id not in {368780147563823114, 700133917264445480}
            or self.config.primary_guild != message.guild.id
        ):
            return

        content = strip_str(message.content)
        if fuzz.partial_ratio(content, "twitter") > 85:
            with suppress(NotFound):
                await message.delete()
            await message.author.send("Trolled")

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        await self.on_twitter(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        await self.on_twitter(after)

    @commands.Cog.listener("on_message")
    async def on_fanfics(self, message: Message):
        if message.author.bot or not message.guild:
            return
        content = strip_str(message.content)
        if re.match(r"(ernie|ernest)readsstartrekfanfic(tion|)(s|)", content):
            await message.delete()
        elif re.match(r"(ernie|ernest)(doesnot|doesn't)readstartrekfanfic(tion|)(s|)", content):
            await message.reply("Based !!!!!!!!!!!!")

    @commands.Cog.listener("on_message")
    async def on_armenium(self, message: Message):
        if message.author.id == self.bot.user.id:
            return
        elif message.channel.id != 811023978045898822 or message.author.id == 232706427045543936:
            return

        await message.delete()
        await message.channel.send(f"{message.author.mention} WTF.", allowed_mentions=allowed_mentions, delete_after=3)


setup = Censorship.basic_setup
