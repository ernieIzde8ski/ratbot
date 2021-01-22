import discord
import discord.ext.commands as commands
from config import logChannel

class direct_messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = bot.get_channel(logChannel)

    @commands.Cog.listener("on_message")
    async def log_message(self, ctx):
        if ctx.author == commands.Bot.user:  return
        elif ctx.guild == None:
            embed=discord.Embed(title=f"Direct Message — {ctx.author} ({ctx.author.id})", description=ctx.content, timestamp=ctx.created_at)
            await self.log_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(direct_messages(bot))
