import discord
import discord.ext.commands as commands
import config

class respuestas(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.corrections = [("bano", "baño")]
        self.dym = "did you mean: "

    @commands.Cog.listener("on_message")
    async def Censorship(self, ctx):
        message = config.cleantext(ctx.content)
        words = ctx.content.split(" ")
        if message and "roblox it you" in message.lower():
            await ctx.delete()
        if ctx.author == commands.Bot.user or ctx.author.bot:  return
        if ctx.guild and ctx.channel.name != "rat":
            # detect slurs & make them only work in whichever servers have opted in

            if config.SlursExist(ctx.content) and (ctx.guild.id in config.guildOptIn):
                print("loser detected")
                await ctx.channel.send(f"loser {ctx.author.mention}")
                return
            # correct ratards
            elif message:
                if not (ctx.guild.id in config.guildOptOut) and "retard" in message.lower():
                    await ctx.channel.send("*ratard")
                    return
    		# kill tenor links lmao
            elif ctx.guild.id in config.guildOptIn and (ctx.content.startswith("https://giphy.com/gifs/") or ctx.content.startswith("https://tenor.com/view/")):
                print("tenor loser detected")
                await ctx.channel.send(f"loser {ctx.author.mention}")
                await ctx.message.delete()
        correction = self.dym
        for i in self.corrections:
            if i[0] in words:
                correction += f"{i[1]}, "
        if correction != self.dym:
            await ctx.channel.send()

def setup(bot):
    bot.add_cog(respuestas(bot))
