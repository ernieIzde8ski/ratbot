from discord.ext import commands


class Respuestas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def censorship(self, msg):
        if msg.author.bot or not msg.guild: return
        if msg.channel.name != "rat":
            # kill tenor links lmao
            if msg.guild.id in self.bot.config.guild_opt_in and (
                    msg.content.startswith("https://giphy.com/gifs/") or msg.content.startswith(
                "https://tenor.com/view/")):
                await msg.channel.send(f"loser {msg.author.mention}")
                await msg.delete()


def setup(bot):
    bot.add_cog(Respuestas(bot))
