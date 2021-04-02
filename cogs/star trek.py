import discord.ext.commands as commands

import modules.SentenceGenerator as SentenceGenerator


class Startrek(commands.Cog):
    """Various Star Trek related commands"""

    def __init__(self, bot):
        self.bot = bot
        self.tos_generator = SentenceGenerator.loadGenerator("modules/StarTrek.txt")
        try:
            self.tng_generator = SentenceGenerator.loadGenerator("modules/StarTrekTNG.txt")
        except ValueError as e:
            print(f"ValueError: {e}")

    @commands.command(hidden=True)
    async def load_trek(self, ctx):
        """reloads the star trek generator, in case changes occurred to StarTrek.txt"""
        self.tos_generator = SentenceGenerator.loadGenerator("modules/StarTrek.txt")
        self.tng_generator = SentenceGenerator.loadGenerator("modules/StarTrekTNG.txt")
        await ctx.send('Reloaded! probably')

    @commands.command(aliases=["tos"])
    async def random_tos(self, ctx, count: int = 1):
        """Generates a randomized Star Trek: TOS plot."""

        if not (1 <= count <= 5):
            await ctx.send(f"1-5 pls (Not {count} Bro)")
            return
        for i in range(count):
            await ctx.send(self.tos_generator.generate())

    @commands.command(aliases=["tng"], hidden=True)
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
        await ctx.send(
            f"We are the {item}. Lower your shields and surrender your ships. We will add your biological and "
            f"technological distinctiveness to our own. Your culture will adapt to service us. Resistance is futile."
        )


def setup(bot):
    bot.add_cog(Startrek(bot))
