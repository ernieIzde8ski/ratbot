import discord.ext.commands as commands
from json import load
from discord import Message
from asyncio import sleep


class Cansti(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.im = ("i'm", "im", "i´m", "i am")
        with open("modules/haddaway.json", "r", encoding="utf-8") as f:
            self.haddaway = load(f)

    @staticmethod
    def isCansti(ctx):
        if not ctx.guild:
            return False
        return ctx.guild.id == 387729240008818689

    @commands.Cog.listener('on_message')
    async def on_haddaway(self, msg):
        if not self.isCansti(msg):
            return
        if msg.content.lower() != "what is love":
            return
        punctuation = ",'?.-–"
        for resp, expected in self.haddaway:
            await sleep(1)
            m = await msg.channel.send(resp.upper())

            async def check(m: Message):
                if m.channel != msg.channel or m.author.id != msg.author.id:
                    return False
                for p in punctuation:
                    m.content = m.content.replace(p, "")
                return m.content.lower() == expected or not expected
            if expected:
                await self.bot.wait_for("message", timeout=30, check=check)
        await m.add_reaction("<:wackyZany:785734170612596748>")


def setup(bot):
    bot.add_cog(Cansti(bot))
