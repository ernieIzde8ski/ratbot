from urllib.parse import quote

import discord
import discord.ext.commands as commands
from typing import Optional, Union

import asyncio
import aiohttp


def birthday_link(name):
    return f"https://itsyourbirthday.today/#{quote(name)}"


async def log(bot, msg: str):
    channel = bot.get_channel(762166605458964510)
    await channel.send(content=msg)


async def get_verse(verse):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://bible-api.com/{quote(verse)}?translation=kjv") as resp:
            respuesta = await resp.json()

            text = ""
            # remove all instances of \n from the verse(s) and make into a list
            word_list = respuesta["text"].replace("\n", " ").split(" ")
            for index, word in enumerate(word_list):
                # append a word & add a new line if twelfth word in a row
                text += f"{word} "
                if (index+1) % 12 == 0:
                    text += "\n"

            return {
                "heading": respuesta["reference"],
                "text": text
            }


class Fun(commands.Cog):
    """Miscellaneous drivellous commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["CC", "cc"])
    async def cringecount(self, ctx, iteration: int = 1):
        """\"Liking liking things is cringe is cringe\""""
        if iteration < 105:
            await ctx.channel.send("""Bro.... Liking {'"Liking ' * int}Things {'Is Cringe" ' * int}is Cringe....""")
        else:
            await ctx.channel.send("no")

    @commands.command(aliases=["bd"])
    async def birthday(self, ctx, recipient: Union[discord.Member, str], *, name: Optional[str]):
        """returns a link to the rat "it's your birthday today" site with a given recipient/name"""
        if not isinstance(recipient, str) and not name:  # if the person is mentioned without additional name
            await ctx.channel.send(f"happy birthday {recipient.mention}! \n{birthday_link(recipient.display_name)}")
        elif not isinstance(recipient, str) and name:  # if the person is mentioned with name
            await ctx.channel.send(f"happy birthday {recipient.mention}! \n{birthday_link(name)}")
        elif isinstance(recipient, str) and not name:
            await ctx.channel.send(f"happy birthday {recipient}! \n{birthday_link(recipient)}")
        elif isinstance(recipient, str) and name:
            await ctx.channel.send(f"happy birthday {recipient}! \n{birthday_link(name)}")

    @commands.command(aliases=["bible", "verse", "v", "🙏"])
    async def bible_verse(self, ctx, *, verse):
        """returns a bible verse or passage from the format book chapter:verse(s)"""
        verse = await get_verse(verse)
        embed = discord.Embed(title=verse["heading"], description=verse["text"],
                              url=f"https://www.biblegateway.com/passage/?search={quote(verse['heading'])}&version=NIV",
                              timestamp=ctx.message.created_at)
        try:
            await ctx.channel.send(embed=embed)
        except discord.errors.HTTPException as e:
            await ctx.channel.send(f"discord.errors.HTTPException: {e}")


def setup(bot):
    bot.add_cog(Fun(bot))
