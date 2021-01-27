import discord.ext.commands as commands

import config


class Respuestas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message")
    async def censorship(self, msg):
        message = config.cleantext(msg.content)
        words = msg.content.split(" ")
        if message and "roblox it you" in message.lower():
            await msg.delete()
        if msg.author == commands.Bot.user or msg.author.bot:  return
        if msg.guild and msg.channel.name != "rat":
            # detect slurs & make them only work in whichever servers have opted in

            if config.SlursExist(msg.content) and (msg.guild.id in config.guildOptIn):
                print("loser detected")
                await msg.channel.send(f"loser {msg.author.mention}")
                return
            # correct ratards
            elif message:
                if not (msg.guild.id in config.guildOptOut) and "retard" in message.lower():
                    await msg.channel.send("*ratard")
                    return
            # kill tenor links lmao
            elif msg.guild.id in config.guildOptIn and (
                    msg.content.startswith("https://giphy.com/gifs/") or msg.content.startswith(
                "https://tenor.com/view/")):
                print("tenor loser detected")
                await msg.channel.send(f"loser {msg.author.mention}")
                await msg.message.delete()


def setup(bot):
    bot.add_cog(Respuestas(bot))

# message from myer: this is the biggest mess of nested ifs i've ever seen and i'm too lazy to figure it out
# cause i'll probably break something so deal with it
