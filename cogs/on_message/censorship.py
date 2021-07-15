import re
from discord import Message, AllowedMentions, NotFound
from discord.ext import commands
from fuzzywuzzy import fuzz

from modules.functions import reduce


class Censorship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_mentions = AllowedMentions.all()

    async def on_twitter(self, message: Message) -> None:
        if not message.guild or message.author.id not in [368780147563823114, 700133917264445480]:
            return
        elif self.bot.config["main_guild"] != message.guild.id:
            return

        content = reduce(message.content)
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
        content = reduce(message.content)
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
        await message.channel.send(f"{message.author.mention} WTF.",
                                   allowed_mentions=self.allowed_mentions,
                                   delete_after=3)

    @commands.Cog.listener("on_message")
    async def on_tenor(self, message: Message):
        if message.author.bot or not message.guild:
            return
        elif message.guild.id not in self.bot.tenor_guilds:
            return
        elif re.match(r"https{0,1}:\/\/(www.)*tenor.com\/view\/([a-z]|-)+\d+", message.content):
            await message.delete()
            await message.channel.send(f"{message.author.mention} Stupid", allowed_mentions=self.allowed_mentions)


def setup(bot):
    bot.add_cog(Censorship(bot))
