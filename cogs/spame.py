from random import random, choice
from typing import Optional

import discord.ext.commands as commands
from discord import Forbidden, HTTPException

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
            if random() < 0.2:
                out_str += choice(replacements[letter])
            else:
                out_str += letter
        if out_str == "spame":
            out_str = ""
            continue
        else:
            return out_str


class Spame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["spame"])
    async def print_spame(self, ctx, count: int = 1):
        """Generate a variation on "spame\""""
        if count > 200:
            await ctx.channel.send("no")
            return
        msg = generate_spame()
        if count != 1:
            for i in range(0, count):
                msg += f", {generate_spame()}"
        await ctx.channel.send(msg)

    @commands.command(aliases=["respame"], hidden=True)
    @commands.has_permissions(manage_nicknames=True)
    async def rename_spame(self, ctx, *, nick: Optional[str]):
        """Renames all users (optionally, only with a given nickname) to variants on "spame"."""
        member_list = ctx.guild.members
        if nick:
            _list = []
            for member in member_list:
                if member.nick == nick:
                    _list.append(member)
                else:
                    continue
            member_list = _list
        successes = [0, 0, 0]
        for member in member_list:
            new_name = generate_spame()
            try:
                await member.edit(nick=new_name)
            except Forbidden:
                successes[1] += 1
            except HTTPException:
                successes[2] += 1
            else:
                successes[0] += 1
        await ctx.channel.send(f"Successfully changed {successes[0]} nick(s)\n"
                               f"{successes[1] + successes[2]} failures ({successes[1]} Forbidden, "
                               f"{successes[2]} HTTPException)")


def setup(bot):
    bot.add_cog(Spame(bot))
