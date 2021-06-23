from discord.ext import commands
from fuzzywuzzy import fuzz

class Nico(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Nico = None
    
    @staticmethod
    def verify(s1: str, s2: str="frick", min: int=65):
        s1 = s1.lower()
        s2 = s2.lower()
        return fuzz.ratio(s1, s2) > min or fuzz.partial_ratio(s1, s2) > min
    
    async def get_nico(self) -> None:
        await self.bot.wait_until_ready()
        self.Nico = self.bot.get_user(302956027656011776)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Reminder to self: update these integers before pushing to server
        # ignore incorrect channels/authors, failing grades
        if message.channel.id != 488479538104369153 or message.author.id != 302956027656011776:
            return
        elif not self.verify(message.content): 
            return
        
        await self.Nico.send("<#488479538104369153>")

def setup(bot):
    cog = Nico(bot)
    bot.loop.create_task(cog.get_nico())
    bot.add_cog(cog)