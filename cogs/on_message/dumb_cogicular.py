import discord.ext.commands as commands


class NicoInforming(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def nico_send(self, m):
        if not (m.channel.id == 758373055918899216 and m.author.id == 544274326002860033 and m.content == "frick"):
            return
        nico = self.bot.get_user(251792286260658196)
        await nico.send(m.channel.mention)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.nico_send(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.nico_send(after)


def setup(bot):
    bot.add_cog(NicoInforming(bot))
