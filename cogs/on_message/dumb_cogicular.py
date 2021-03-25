import discord.ext.commands as commands


class NicoInforming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.channel.id != 758373055918899216 or msg.author.id != 544274326002860033:
            return
        if msg.content == "frick":
            nico = self.bot.get_member(251792286260658196)
            await nico.send(msg.channel.mention)


def setup(bot):
    bot.add_cog(NicoInforming(bot))
