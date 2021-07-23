from aiohttp import ClientSession
from discord import Embed
from discord.ext import commands
from textwrap import fill
from typing import Optional

from modules._json import safe_load, safe_dump
from modules.converters import StrictBool


class Bible(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translation_languages = {"cherokee": ["Cherokee New Testament", "Cherokee"],
                                      "kjv": ["King James Version", "English"],
                                      "web": ["World English Bible", "English"],
                                      "clementine": ["Clementine Latin Vulgate", "Latine"],
                                      "almeida": ["João Ferreira de Almeida", "Português"],
                                      "rccv": ["Romanian Corrected Cornilescu Bible", "Română"]}
        self.valid_translations = self.translation_languages.keys()
        self.data = safe_load("data/bible.json", {})

    @staticmethod
    async def get_text(reference, translation, characters_per_line: int = 70, display_verse_number: bool = False) -> dict:
        """Retrieve a verse or verses & return its relevant contents"""
        async with ClientSession() as session:
            async with session.get(f"https://bible-api.com/{reference}?translation={translation}") as resp:
                resp = await resp.json()

                if resp.get("error"):
                    return {"error": resp["error"]}
                elif isinstance(resp, str):
                    return {"error": resp}

                if display_verse_number is False:
                    content = resp["text"]
                else:
                    verses = [verse["text"].replace("\n", "") for verse in resp["verses"]]
                    verses = map(lambda verse: f"**{verse['verse']}** {verse['text']}", resp["verses"])
                    content = " ".join(verses)

                return {
                    "reference": resp["reference"],
                    "content": fill(content, width=characters_per_line),
                    "translation": resp["translation_name"]
                }

    @staticmethod
    def embed_constructor(text: dict, color, display_footer_hint: bool) -> Embed:
        url = "https://biblegateway.com/passage/?search={}&version=NIV"
        footer = f"Translation: {text['translation']}"
        if display_footer_hint == True:
            footer += " | If this version is difficult or this message too annoying, you can click the link or use the set_translation command"
        return Embed(
            title=text["reference"],
            description=text["content"],
            color=color,
            url=url.format(text["reference"].replace(" ", "%20"))
        ).set_footer(text=footer)

    @commands.command(aliases=["v", "🙏"])
    async def bible_verse(self, ctx, display_verse: Optional[StrictBool] = True, *, reference: str = "Joshua 21:8"):
        """Returns a passage based off a reference"""
        if (translation := self.data.get(str(ctx.author.id))) is None:
            translation = "KJV"
            translation_not_set = True
        else:
            translation_not_set = False

        text = await self.get_text(reference, translation, display_verse_number=display_verse)

        if text.get("error"):
            raise commands.CommandError(text['error'])
        elif text["content"].__len__() > 1000:
            reference = text["reference"].replace(' ', "%20")
            error = f"Passage is too long.\nTry: <https://biblegateway.com/passage/?search={reference}>"
            raise commands.CommandError(error)
        else:
            await ctx.send(embed=self.embed_constructor(text, ctx.me.color, translation_not_set))

    @commands.command(aliases=["set_version"])
    async def set_translation(self, ctx, *, translation: Optional[str]):
        """Sets a version to use in the bible_verse command
        Due to the limitations of the api I use (https://bible-api.com/),
        there's only a few functional translations (displayed by invoking
        the command)."""
        if translation:
            translation = translation.lower()
        if not translation:
            await ctx.send(f"Available translations: `{'`, `'.join(self.valid_translations)}`")
        elif translation not in self.valid_translations:
            await ctx.send(
                f"Invalid translation!\n"
                f"Available translations: `{'`, `'.join(self.valid_translations)}`"
            )
        else:
            self.data[str(ctx.author.id)] = translation
            safe_dump("data/bible.json", self.data)
            translation = f"`{self.translation_languages[translation][0]}` ({self.translation_languages[translation][1]})"
            await ctx.send(f"Set your translation to {translation}")


def setup(bot):
    bot.add_cog(Bible(bot))
