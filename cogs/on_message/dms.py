import discord
from discord.ext import commands


class DM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def log_message(self, msg):
        if msg.guild: return
        if msg.author == self.bot.user:
            embed = discord.Embed(title=f"Direct Message → {msg.channel.recipient} ({msg.channel.recipient.id})",
                                  description=msg.content, timestamp=msg.created_at, color=discord.Color.orange())
            await self.bot.config.channels.log.send(embed=embed)
        if msg.author.bot:
            return
        else:
            embed = discord.Embed(title=f"Direct Message — {msg.author} ({msg.author.id})",
                                  description=msg.content, timestamp=msg.created_at, color=discord.Color.dark_blue())
            await self.bot.config.channels.log.send(embed=embed)


def setup(bot):
    bot.add_cog(DM(bot))
