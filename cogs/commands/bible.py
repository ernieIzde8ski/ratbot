import typing
from typing import Optional

from discord import Embed
from discord.ext import commands
from modules._json import safe_dump, safe_load
from modules.converters import StrictBool

from cogs.commands._bible.fetch import BibleError, PassageRetrieval


class Bible(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.valid_translations = {
            "cherokee": ["Cherokee New Testament", "Cherokee"],
            "bbe": ["Bible in Basic English", "English"],
            "kjv": ["King James Version", "English"],
            "oeb-us": ["Open English Bible", "English (US)"],
            "oeb-cw": ["Open English Bible", "English (UK)"],
            "web": ["World English Bible", "English"],
            "webbe": ["World English Bible", "English (UK)"],
            "clementine": ["Clementine Latin Vulgate", "Latine"],
            "almeida": ["João Ferreira de Almeida", "Português"],
            "rccv": ["Romanian Corrected Cornilescu Bible", "Română"]
        }
        self.valid_translation_keys = self.valid_translations.keys()
        self.valid_translations_str = "Available translations: `" + "`, `".join(self.valid_translation_keys) + "`"
        self.data: typing.Dict = safe_load("data/bible.json", {})
        self.session = PassageRetrieval()

    @commands.command(aliases=["v", "🙏"])
    async def bible_verse(self, ctx: commands.Context, display_verse: Optional[StrictBool] = True, *, reference: str = "Joshua 21:8"):
        """Returns a passage based off a reference"""

        translation = self.data.get(str(ctx.author.id))

        resp = await self.session.procget(reference, translation=translation, verse_numbers=display_verse)
        url = f"https://biblegateway.com/passage/?search={resp.ref.replace(' ', '%20')}&version=NIV"

        if len(resp.text) > 1200:
            raise BibleError(f"Passage is too long.\nTry: <{url}>")

        footer = f"Translation: {resp.tr.name}"
        if translation is None:
            footer += " | If this version is difficult or this message too annoying," \
                      " you can click the link or use {}set_translation KJV".format(ctx.prefix)

        embed = Embed(
            title=resp.ref, description=resp.text, color=ctx.me.color, url=url
        ).set_footer(text=footer)
        await ctx.send(embed=embed)

    @commands.command(aliases=["set_version"])
    async def set_translation(self, ctx: commands.Context, *, translation: Optional[str]):
        """Sets a version to use in the bible_verse command
        Due to the limitations of the api I use (https://bible-api.com/),
        there's only a few functional translations (displayed by invoking
        the command)."""
        print(0)
        if not translation:
            return await ctx.send(self.valid_translations_str)

        print(1)
        translation = translation.lower()

        print(2)
        if translation not in self.valid_translation_keys:
            return await ctx.send("Invalid translation!\n" + self.valid_translations_str)

        print(3)
        self.data[str(ctx.author.id)] = translation
        safe_dump("data/bible.json", self.data)
        print(4)
        translation = f"`{self.valid_translations[translation][0]}` [{self.valid_translations[translation][1]}]"
        await ctx.send(f"Set your translation to {translation}")
        print(5)


def setup(bot):
    bot.add_cog(Bible(bot))
