import discord.ext.commands as commands
from discord import AllowedMentions


class Respuestas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tenor = ("https://giphy.com/gifs/", "https://tenor.com/view/")

    @commands.Cog.listener("on_message")
    async def censorship(self, msg):
        if msg.author.bot or not msg.guild: return
        if msg.channel.name != "rat":
            # kill tenor links lmao
            if msg.guild.id in self.bot.config.guild_opt_in and msg.content.startswith(self.tenor):
                await msg.channel.send(f"loser {msg.author.mention}", allowed_mentions=AllowedMentions(users=True))
                await msg.delete()


def setup(bot):
    bot.add_cog(Respuestas(bot))
