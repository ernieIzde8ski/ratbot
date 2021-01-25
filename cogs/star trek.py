import discord
import discord.ext.commands as commands
import modules.SentenceGenerator as SentenceGenerator
from typing import Optional


class startrek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            self.tos_generator = SentenceGenerator.loadGenerator("modules/StarTrek.txt")
            self.tng_generator = SentenceGenerator.loadGenerator("modules/StarTrekTNG.txt")
        except:
            print("Lol TNG Proaly Not working")

    @commands.command(hidden=True)
    async def load_trek(self, ctx):
        """reloads the star trek generator, in case changes occurred to StarTrek.txt"""
        self.tos_generator = SentenceGenerator.loadGenerator("modules/StarTrek.txt")
        self.tng_generator = SentenceGenerator.loadGenerator("modules/StarTrekTNG.txt")
        await ctx.send('Reloaded! probably')

    @commands.command(aliases = ["tos"])
    async def random_tos(self, ctx, count: int = 1):
        """Generates a randomized Star Trek: TOS plot."""

        if not (1 <= count <= 5):
            await ctx.send(f"1-5 pls (Not {count} Bro)")
            return
        for i in range(count):
            await ctx.send(self.tos_generator.generate())

    @commands.command(aliases = ["tng"])
    async def random_tng(self, ctx, count: int = 1):
        """Generates a randomized Star Trek: TNG plot."""
        if not (1 <= count <= 5):
            await ctx.send(f"1-5 pls (Not {count} Bro)")
            return
        for i in range(count):
            await ctx.send(self.tng_generator.generate())

    @commands.command()
    async def borg(self, ctx, *, item: str):
        """Generates a borg phrase dependent on your input."""
        await ctx.send(f"We are the {item}. Lower your shields and surrender your ships. We will add your biological and technological distinctiveness to our own. Your culture will adapt to service us. Resistance is futile.", allowed_mentions=discord.AllowedMentions.none())


def setup(bot):
    bot.add_cog(startrek(bot))