import discord.ext.commands as commands

import config


class Respuestas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def censorship(self, msg):
        if msg.author.bot or not msg.guild: return
        if msg.channel.name != "rat":
            # kill tenor links lmao
            elif msg.guild.id in config.guildOptIn and (
                    msg.content.startswith("https://giphy.com/gifs/") or msg.content.startswith(
                "https://tenor.com/view/")):
                await msg.channel.send(f"loser {msg.author.mention}")
                await msg.message.delete()


def setup(bot):
    bot.add_cog(Respuestas(bot))

# message from myer: this is the biggest mess of nested ifs i've ever seen and i'm too lazy to figure it out
# cause i'll probably break something so deal with it
