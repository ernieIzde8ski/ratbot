from asyncio import sleep
from random import random

import discord
from discord.ext import commands
from utils import RatCog


class Bans(RatCog):
    """Random bans serviced by your local Rat Bot"""

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if (
            not message.guild
            or message.author == self.bot.user
            or (chance := self.guilds[message.guild.id].ban_chance) is None
            or random() > chance
        ):
            return

        message = await message.reply("Uh Oh", allowed_mentions=self.bot._all_mentions)
        await sleep(7)
        try:
            await message.author.ban()
        except discord.Forbidden:
            await message.reply("OK Nevermind", allowed_mentions=self.bot._all_mentions)


setup = Bans.basic_setup
