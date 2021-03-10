import discord.ext.commands as commands


class Rata(commands.Cog):
      """Wonder if putting a docstring here does anything"""
      def __init__(self, bot):
            """or here"""
            self.bot = bot

      @commands.Cog.listener()
      async def on_message(self, msg):
            if msg.channel.name == "rata" and msg.content != "rata":
                  await msg.delete()
                  return
            elif msg.author.bot: return
            elif msg.content == "rata":
                  await msg.channel.send("rata")

def setup(bot):
      bot.add_cog(Rata(bot))