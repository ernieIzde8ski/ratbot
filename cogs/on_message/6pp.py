import random
import discord.ext.commands as commands
from discord import errors
from asyncio import sleep


class Banned(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot or ctx.channel.id != 825067717106466916:
            return
        else:
            value = random.randint(0, 200)
            if value == 0:
                await ctx.channel.send(f"{ctx.author.mention} Uh Oh")
                await sleep(3)
                try:
                    await ctx.guild.ban(ctx.author, delete_message_days=0, reason="Lobbled")
                except errors.Forbidden:
                    await ctx.channel.send("Fropple...........")


def setup(bot):
    bot.add_cog(Banned(bot))
