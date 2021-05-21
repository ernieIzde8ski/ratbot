from urllib.parse import quote

import discord.ext.commands as commands
from aiohttp import ClientSession
from discord import Color, Embed


def get_bg_link(reference: str, translation: str = "NIV") -> str:
    return (f"https://www.biblegateway.com/passage/"
            f"?search={quote(reference)}"
            f"&version={quote(translation)}")


async def get_verse(verse, words_per_line: int = 8, text_translation: str = "KJV",
                    link_translation: str = "NIV") -> dict:
    async with ClientSession() as session:
        async with session.get(f"https://bible-api.com/{verse}?translation={text_translation}") as resp:
            resp = await resp.json()

            if resp.get("error"):
                return {"heading": None, "text": f"error: {resp['error']}", "url": None}

            if len(resp["text"]) > 1000:
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
                word_list = resp["text"].replace("\n", " ").split(" ")
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
                "heading": resp["reference"],
                "text": text,
                "url": get_bg_link(verse, link_translation)
            }


async def get_random_verse() -> str:
    async with ClientSession() as session:
        async with session.get(f"https://labs.bible.org/api/?passage=random&type=json") as resp:
            resp = (await resp.json(content_type="application/x-javascript"))[0]
            return f"{resp['bookname']} {resp['chapter']}:{resp['verse']}"


class Bible(commands.Cog):
    """Bible command"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=["bible", "verse", "v", "🙏"], invoke_without_command=True)
    async def bible_verse(self, ctx, *, reference):
        """returns a bible verse or passage from the format 'book chapter:verse(s)'"""
        verses = await get_verse(reference)
        embed = Embed(
            title=verses["heading"],
            description=verses["text"],
            url=verses["url"],
            color=Color.dark_orange()
        )
        await ctx.channel.send(embed=embed)

    @bible_verse.command(aliases=["r"])
    async def random(self, ctx):
        reference = await get_random_verse()
        verses = await get_verse(reference)
        embed = Embed(
            title=verses["heading"],
            description=verses["text"],
            url=verses["url"],
            color=Color.dark_orange()
        )
        await ctx.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Bible(bot))
