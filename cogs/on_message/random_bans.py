from discord.ext import commands
from discord import Message, AllowedMentions, Forbidden
from asyncio import sleep
from modules._json import safe_load, safe_dump
from modules.converters import Percentage
from typing import Optional
from random import random


class Bans(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guilds = safe_load("data/banning.json", {})

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def toggle_random_bans(self, ctx, percent: Optional[Percentage]):
        if not ctx.guild:
            return await ctx.send("You need to be in a guild for this!")

        id = str(ctx.guild.id)
        if id in self.guilds and not percent:
            await ctx.send("Disabling random bans in this guild")
            self.guilds.pop(id)
        else:
            if not percent:
                percent = 0.00002
            elif not (0 < percent < 1):
                return await ctx.send("Error: Percentage must be from 0% to 100% (or 0.0 to 1.0)")
            await ctx.send(f"Enabling random bans in this guild with a {percent * 100}% chance")
            self.guilds[id] = percent
        safe_dump("data/banning.json", self.guilds)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        if not message.guild:
            return

        guild_id = str(message.guild.id)
        if guild_id not in self.guilds:
            return
        elif random() > self.guilds[guild_id]:
            return

        message = await message.reply("Uh Oh", allowed_mentions=AllowedMentions.all())
        await sleep(7)
        try:
            await message.author.ban()
        except Forbidden:
            await message.reply("OK Nevermind", allowed_mentions=AllowedMentions.all())


def setup(bot):
    bot.add_cog(Bans(bot))
