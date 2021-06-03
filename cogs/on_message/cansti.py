import discord.ext.commands as commands
from json import load
from discord import Message
from asyncio.exceptions import TimeoutError

class Cansti(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.im = ("i'm", "im", "i´m", "i am")
        with open("modules/haddaway.json", "r", encoding="utf-8") as f:
            self.haddaway = load(f)
        self.haddaway_running = False

    @staticmethod
    def isCansti(ctx):
        if not ctx.guild:
            return False
        return ctx.guild.id == 271034455462772737

    @commands.Cog.listener('on_message')
    async def on_haddaway(self, msg):
        if msg.author.bot or not self.isCansti(msg):
            return

        punctuation = [',', "'", '?', '.', '-', '–', "(oooh)", "(uh, uh)"]
        msg.content = msg.content.lower()
        for p in punctuation:
            msg.content = msg.content.replace(p, "")
        if msg.content != "what is love" or self.haddaway_running:
            return

        self.haddaway_running = True
        for resp, expected in self.haddaway:
            m = await msg.channel.send(resp.upper())

            def check(m: Message):
                if m.channel != msg.channel or m.author.id != msg.author.id:
                    return False
                m.content = m.content.lower()
                for p in punctuation:
                    m.content = m.content.replace(p, "")
                content = m.content.replace("  ", " ").strip()
                return content == expected or not expected
            
            if expected:
                try:
                    await self.bot.wait_for("message", timeout=30, check=check)
                except TimeoutError:
                    await msg.channel.send("Bitch")
                    self.haddaway_running = False
                    return
        
        # Respond once complete
        await m.add_reaction("<:wackyZany:785734170612596748>")
        self.haddaway_running = False

def setup(bot):
    bot.add_cog(Cansti(bot))
