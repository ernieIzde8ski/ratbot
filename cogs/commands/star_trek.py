import random
from discord.ext import commands

from modules.SentenceGenerator import loadGenerator
from modules._json import safe_load


class Trek(commands.Cog):
    def __init__(self):
        self.tos_generator = loadGenerator("modules/JSON/Star_Trek.meow")
        self.borg_samples = safe_load("modules/JSON/borg.json", [])

    @commands.command()
    async def borg(self, ctx, *, borg: str = "Borg"):
        """Sends a Borg copypasta with an argument as Borg"""
        resp = "We are the {Borg}. "
        resp += " ".join(random.sample(self.borg_samples,
                                       k=random.randint(2, len(self.borg_samples))
        ))
        await ctx.send(resp.format(Borg=borg, Locutus=ctx.author.display_name.title()))

    @commands.command(aliases=["rt", "trek"])
    async def random_tos_plot(self, ctx, count: int = 1):
        """Generates a random Star Trek: The Original Series plot"""
        if not (1 <= count <= 10):
            raise commands.BadArgument("Parameter \"count\" must range from 1 to 10.")

        resp = ""
        for i in range(count):
            resp += self.tos_generator.generate() + "\n"
        await ctx.send(resp)


def setup(bot):
    bot.add_cog(Trek())
