import re

from discord import AllowedMentions, Message, NotFound
from discord.ext import commands
from fuzzywuzzy import fuzz
from utils.classes import RatBot
from utils.functions import strip_str

tenor_pattern = re.compile(r"https{0,1}:\/\/(www.)*tenor.com\/view\/([a-z]|-)+\d+")


class Censorship(commands.Cog):
    def __init__(self, bot: RatBot):
        self.bot = bot
        self.allowed_mentions = AllowedMentions.all()

    async def on_twitter(self, message: Message) -> None:
        if not message.guild or message.author.id not in [368780147563823114, 700133917264445480]:
            return
        elif self.bot.config["primary_guild"] != message.guild.id:
            return

        content = strip_str(message.content)
        if fuzz.partial_ratio(content, "twitter") > 85:
            try:
                await message.delete()
            except NotFound:
                pass
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
        await message.channel.send(
            f"{message.author.mention} WTF.", allowed_mentions=self.allowed_mentions, delete_after=3
        )

    @commands.Cog.listener("on_message")
    async def on_tenor(self, message: Message):
        if message.author.bot or not message.guild:
            return
        elif message.guild.id not in self.bot.data.tenor_guilds:
            return
        elif re.match(tenor_pattern, message.content):
            await message.delete()
            await message.channel.send(f"{message.author.mention} Stupid", allowed_mentions=self.allowed_mentions)


def setup(bot: RatBot):
    bot.add_cog(Censorship(bot))
