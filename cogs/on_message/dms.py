import discord
from discord.ext import commands
from typing import Union


class DM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.latest = None

    @commands.Cog.listener()
    async def on_message(self, msg):
        # pass only if in direct messages
        if msg.guild: return
        # log own messages as an embed in the proper channel
        if msg.author == self.bot.user:
            embed = discord.Embed(title=f"Direct Message → {msg.channel.recipient} ({msg.channel.recipient.id})",
                                  description=msg.content, timestamp=msg.created_at, color=discord.Color.orange())
            return await self.bot.config.channels.log.send(embed=embed)
        # log message only if is not bot user
        elif msg.bot.user: return
        else:
            embed = discord.Embed(title=f"Direct Message — {msg.author} ({msg.author.id})",
                                  description=msg.content, timestamp=msg.created_at, color=discord.Color.dark_blue())
            # also save for later
            self.latest = msg
            await self.bot.config.channels.log.send(embed=embed)

    @commands.command(aliases=["vessel", "wessel"])
    @commands.is_owner()
    async def echo(self, ctx, messageable: Union[commands.TextChannelConverter, commands.UserConverter, int, None], *,
                   text: str):
        """Bogstandard echo command"""
        if type(messageable) is int or not messageable:
            messageable = self.bot.get_channel(messageable) if (type(messageable) is int) else ctx.channel
        await messageable.send(text)


def setup(bot):
    bot.add_cog(DM(bot))
