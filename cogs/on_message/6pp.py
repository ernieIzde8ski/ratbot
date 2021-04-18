from asyncio import sleep
from random import random

import discord.ext.commands as commands
from discord import errors, AllowedMentions


class Banned(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot or ctx.guild.id not in self.bot.config.SixPP_guilds:
            return
        else:
            if random() <= self.bot.config.SixPP_Chance:
                await ctx.channel.send(f"{ctx.author.mention} Uh Oh", allowed_mentions=AllowedMentions(users=True))
                await sleep(10)
                try:
                    await ctx.guild.ban(ctx.author, delete_message_days=0, reason="Lobbled")
                except errors.Forbidden:
                    await ctx.channel.send("Fropple...........")


def setup(bot):
    bot.add_cog(Banned(bot))
