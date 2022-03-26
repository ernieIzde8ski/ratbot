import random

from discord.ext import commands
from utils import RatBot, RatCog, SentenceGenerator, safe_load


class Trek(RatCog):
    def __init__(self, bot: RatBot):
        super().__init__(bot=bot)
        self.tos_generator = SentenceGenerator.loadGenerator("utils/JSON/Star_Trek.meow")
        self.borg_samples = safe_load("utils/JSON/borg.json", [])
        self.borglen = len(self.borg_samples)

    @commands.command()
    async def borg(self, ctx: commands.Context, *, borg: str = "Borg"):
        """Sends a Borg copypasta with an argument as Borg"""
        resp = random.choices(["We are the {Borg}. ", "I am {Locutus} of {Borg}. "], [2, 1], k=1)[0]
        resp += " ".join(random.sample(self.borg_samples, k=random.randint(2, self.borglen)))
        await ctx.send(resp.format(Borg=borg, Locutus=ctx.author.display_name.title()))

    @commands.command(aliases=["rt", "trek"])
    async def random_tos_plot(self, ctx: commands.Context, count: int = 1):
        """Generates a random Star Trek: The Original Series plot"""
        if not (1 <= count <= 10):
            raise commands.BadArgument('Parameter "count" must range from 1 to 10.')

        resp = "".join(self.tos_generator.generate() + "\n" for _ in range(count))
        await ctx.send(resp)


setup = Trek.basic_setup
