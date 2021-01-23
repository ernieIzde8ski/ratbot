import discord
import discord.ext.commands as commands
from config import logChannel

class direct_messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log_channel = bot.get_channel(logChannel)

    @commands.Cog.listener("on_message")
    async def log_message(self, msg):
        if message.author.bot:  return
        if not self.log_channel: self.log_channel = bot.get_channel(logChannel)
        elif msg.guild == None:
            embed=discord.Embed(title=f"Direct Message — {msg.author} ({msg.author.id})", description=msg.content, timestamp=msg.created_at)
            await self.log_channel.send(embed=embed)

def setup(bot):
    bot.add_cog(direct_messages(bot))
