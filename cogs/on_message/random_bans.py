from asyncio import sleep
from random import random

import discord
from discord.ext import commands
from utils import RatBot, RatCog


class Bans(RatCog):
    """Random bans serviced by your local Rat Bot"""

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not message.guild or message.author == self.bot.user:
            return

        guild_id = str(message.guild.id)
        if guild_id not in self.bot.data.banning_guilds:
            return
        elif random() > self.bot.data.banning_guilds[guild_id]:
            return

        message = await message.reply("Uh Oh", allowed_mentions=self.bot._all_mentions)
        await sleep(7)
        try:
            await message.author.ban()
        except discord.Forbidden:
            await message.reply("OK Nevermind", allowed_mentions=self.bot._all_mentions)


def setup(bot: RatBot):
    bot.add_cog(Bans(bot))
