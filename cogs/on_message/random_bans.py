from asyncio import sleep
from random import random

from discord import AllowedMentions, Forbidden, Message
from discord.ext import commands
from utils.classes import RatBot, RatCog


class Bans(RatCog):
    """Random bans serviced by your local Rat Bot"""

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if not message.guild or message.author == self.bot.user:
            return

        guild_id = str(message.guild.id)
        if guild_id not in self.bot.data.banning_guilds:
            return
        elif random() > self.bot.data.banning_guilds[guild_id]:
            return

        message = await message.reply("Uh Oh", allowed_mentions=AllowedMentions.all())
        await sleep(7)
        try:
            await message.author.ban()
        except Forbidden:
            await message.reply("OK Nevermind", allowed_mentions=AllowedMentions.all())


def setup(bot: RatBot):
    bot.add_cog(Bans(bot))
