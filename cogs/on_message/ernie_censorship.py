from asyncio import sleep
import discord
import discord.ext.commands as commands


class Censorship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot: return
        if ctx.author.id != 232706427045543936 and ctx.channel.id == 811023978045898822:
            await ctx.delete()
            await ctx.channel.send(f"use reactions Idiot {ctx.author.mention}",
                                   allowed_mentions=discord.AllowedMentions(users=True),
                                   delete_after=3)
        else: return


def setup(bot):
    bot.add_cog(Censorship(bot))
