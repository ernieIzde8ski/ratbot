import random
import discord
from discord.ext import commands
import modules.SentenceGenerator as SentenceGenerator


class startrek(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.generator = SentenceGenerator.loadGenerator("modules/StarTrek.txt")

    @commands.command()
    async def load_trek(self, ctx):
        self.generator = SentenceGenerator.loadGenerator("modules/StarTrek.txt")
        await ctx.send('Reloaded! probably')

    @commands.command()
    async def random_tos(self, ctx):
        try:
            await ctx.send(self.generator.generate())
        except:
            await ctx.send('An error occurred! so sad')


def setup(bot):
    bot.add_cog(startrek(bot))
