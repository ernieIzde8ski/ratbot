import discord
import discord.ext.commands as commands


class Censorship(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if message.author.id != 232706427045543936 and message.channel.id == 811023978045898822:
            await message.delete()
            await message.channel.send(
                f"use reactions Idiot {message.author.mention}",
                allowed_mentions=discord.AllowedMentions(users=True),
                delete_after=3
            )


def setup(bot):
    bot.add_cog(Censorship(bot))
