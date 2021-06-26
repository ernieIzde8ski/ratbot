from discord.ext import commands
from modules.SentenceGenerator import loadGenerator
from modules.json import safe_load
import random


class Trek(commands.Cog):
    def __init__(self):
        self.tos_generator = loadGenerator("modules/Star Trek.meow")
        self.borg_samples = safe_load("modules/borg.json", [])

    @commands.command()
    async def borg(self, ctx, *, borg: str = "Borg"):
        resp = "We are the {Borg}. "
        resp += " ".join(random.sample(self.borg_samples,
                         k=random.randint(2, len(self.borg_samples))))
        await ctx.send(resp.format(Borg=borg, Locutus=ctx.author.display_name.title()))

    @commands.command(aliases=["rt", "trek"])
    async def random_tos_plot(self, ctx, count: int = 1):
        if count < 1 or count > 10:
            return await ctx.send("Count must be between 1 and 10")

        resp = ""
        for i in range(count):
            resp += self.tos_generator.generate() + "\n"
        await ctx.send(resp)


def setup(bot):
    bot.add_cog(Trek())
