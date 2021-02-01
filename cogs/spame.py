from discord.ext import commands
from typing import Optional
import random

replacements = {
    "s": ["ś", "ṥ", "ŝ", "š", "ṧ", "s̈", "ṡ", "ş", "ṣ", "ṩ", "ș", "ꞩ", "ȿ", "ᶊ", "ß", "с"],
    "p": ["ṕ", "ṗ", "ᵽ", "ꝑ", "ꝓ", "ꝕ", "p̃", "ᵱ", "ᶈ", "п"],
    "a": ["á", "ä", "à", "ã", "â", "ă", "å", "ȧ", "ą", "ā", "ȃ", "ạ", "ḁ", "ⱥ", "ᶏ", "æ", "α"],
    "m": ["ḿ", "m̋", "ṁ", "ṃ", "m̃", "ᵯ", "ᶆ", "ɱ", "ꬺ", "м", "ⲙ"],
    "e": ["é", "è", "ĕ", "ê", "ễ", "ê̌", "ë", "ẽ", "ė", "ȩ", "ē", "ḛ", "ɇ", "e̩", "ᶒ", "ᶒ", "ꬴ", "ꬳ", "э", "ə", "ɛ"]
}


def generate_spame():
    out_str = ""
    while True:
        for letter in "spame":
            if random.random() < 0.2:
                out_str += random.choice(replacements[letter])
            else:
                out_str += letter
        if out_str == "spame":
            out_str = ""
            continue
        else: return out_str


class Spame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["spame"])
    async def print_spame(self, ctx, count: int = 1):
        if count > 200:
            await ctx.channel.send("no")
            return
        msg = generate_spame()
        if count != 1:
            for i in range(1, (count-1)):
                msg += f", {generate_spame()}"
        await ctx.channel.send(msg)


def setup(bot):
    bot.add_cog(Spame(bot))
