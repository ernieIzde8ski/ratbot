from urllib.parse import quote

import discord.ext.commands as commands
from aiohttp import ClientSession
from discord import AllowedMentions, Color, Embed, errors


def get_bg_link(reference: str, translation: str = "NIV"):
    return (f"https://www.biblegateway.com/passage/"
            f"?search={quote(reference)}"
            f"&version={quote(translation)}")


async def get_verse(verse, words_per_line: int = 8, text_translation: str = "KJV", link_translation: str = "NIV"):
    async with ClientSession() as session:
        async with session.get(f"https://bible-api.com/{verse}?translation={text_translation}") as resp:
            respuesta = await resp.json()

            if len(respuesta["text"]) > 1000:
                return {
                    "heading": "error: text is too long",
                    "text": "click [here]({}) for NKJV, [here]({}) for NIV".format(
                        get_bg_link(verse, "NKJV"), get_bg_link(verse, "NIV")
                    ),
                    "url": get_bg_link(verse, "KJV")
                }

            text = ""
            # remove all instances of \n from the verse(s) and make into a list
            try:
                word_list = respuesta["text"].replace("\n", " ").split(" ")
            except KeyError as e:
                return {
                    "heading": f"KeyError: {e}",
                    "text": "did you perhaps not write the verse correctly ?",
                    "url": None
                }

            for index, word in enumerate(word_list):
                # append a word & add a new line if xth word in a row
                text += f"{word} "
                if (index + 1) % words_per_line == 0:
                    text += "\n"

            return {
                "heading": respuesta["reference"],
                "text": text,
                "url": f"https://www.biblegateway.com/passage/"
                       f"?search={quote(respuesta['reference'])}"
                       f"&version={link_translation}"
            }


class Fun(commands.Cog):
    """Miscellaneous drivellous commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def everyone(self, ctx):
        """Mentions @everyone"""
        await ctx.channel.send("@everyone", allowed_mentions=AllowedMentions(everyone=True))

    @commands.command(aliases=["CC", "cc"])
    async def cringecount(self, ctx, iteration: int = 1):
        """\"Liking liking things is cringe is cringe\""""
        if iteration < 105:
            try:
                await ctx.channel.send(
                    f"Bro.... Liking {'“Liking ' * iteration}Things {'Is Cringe” ' * iteration}is Cringe...."
                )
            except commands.errors.CommandInvokeError as e:
                await ctx.channel.send(f"CommandInvokeError: {e}")
        else:
            await ctx.channel.send("no")

    @commands.command(aliases=["bible", "verse", "v", "🙏"])
    async def bible_verse(self, ctx, *, verse):
        """returns a bible verse or passage from the format book chapter:verse(s)"""
        verse = await get_verse(verse)
        embed = Embed(
            title=verse["heading"],
            description=verse["text"],
            url=verse["url"],
            timestamp=ctx.message.created_at,
            color=Color.dark_orange()
        )
        try:
            await ctx.channel.send(embed=embed)
        except errors.HTTPException as e:
            await ctx.channel.send(f"discord.errors.HTTPException: {e}")


def setup(bot):
    bot.add_cog(Fun(bot))
