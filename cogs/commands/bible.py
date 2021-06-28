from textwrap import fill
from aiohttp import ClientSession
from discord.ext import commands
from json import dump
from modules._json import safe_load
from discord import Embed
from typing import Optional


class Bible(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translation_languages = {"cherokee": ["Cherokee New Testament", "Cherokee"], "kjv": ["King James Version", "English"],
                                      "web": ["World English Bible", "English"], "clementine": ["Clementine Latin Vulgate", "Latine"],
                                      "almeida": ["João Ferreira de Almeida", "Português"], "rccv": ["Romanian Corrected Cornilescu Bible","Română"]}
        self.valid_translations = self.translation_languages.keys()
        self.data = safe_load("data/bible.json", {})

    @staticmethod
    async def get_text(reference, translation, characters_per_line: int = 70) -> dict:
        async with ClientSession() as session:
            async with session.get(f"https://bible-api.com/{reference}?translation={translation}") as resp:
                resp = await resp.json()

                if resp.get("error"):
                    return {"error": resp["error"]}
                elif isinstance(resp, str):
                    return {"error": resp}

                return {
                    "reference": resp["reference"],
                    "content": fill(resp["text"], width=characters_per_line),
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
    async def bible_verse(self, ctx, *, reference: str = "Joshua 21:8"):
        """Returns a passage based off a reference"""
        if self.data.get(str(ctx.author.id)):
            translation = self.data[str(ctx.author.id)]
            translation_not_set = False
        else:
            translation = "KJV"
            translation_not_set = True

        text = await self.get_text(reference, translation)

        if text.get("error"):
            return await ctx.send(f"error: {text['error']}")
        elif text["content"].__len__() > 1000:
            reference = text["reference"].replace(' ', "%20")
            return await ctx.send(f"error: passage is too long\ntry https://biblegateway.com/passage/?search={reference}")
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
            with open("data/bible.json", "w") as file:
                dump(self.data, file)
            await ctx.send(f"Set your translation to `{self.translation_languages[translation][0]}` ({self.translation_languages[translation][1]})")


def setup(bot):
    bot.add_cog(Bible(bot))
