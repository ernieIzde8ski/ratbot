from typing import Optional

from discord import Embed
from discord.ext import commands
from utils import RatCog, StrictBool

from cogs.commands._bible.fetch import BibleError, PassageRetrieval


valid_translations = {
    "cherokee": ["Cherokee New Testament", "Cherokee"],
    "bbe": ["Bible in Basic English", "English"],
    "kjv": ["King James Version", "English"],
    "oeb-us": ["Open English Bible", "English (US)"],
    "oeb-cw": ["Open English Bible", "English (UK)"],
    "web": ["World English Bible", "English"],
    "webbe": ["World English Bible", "English (UK)"],
    "clementine": ["Clementine Latin Vulgate", "Latine"],
    "almeida": ["João Ferreira de Almeida", "Português"],
    "rccv": ["Romanian Corrected Cornilescu Bible", "Română"],
}

valid_translation_keys = valid_translations.keys()
valid_translations_str = "Available translations: `" + "`, `".join(valid_translations) + "`"


class Bible(RatCog):
    # TODO: Maybe make an API for this too
    session = PassageRetrieval()

    @commands.command(aliases=["v", "🙏"])
    async def bible_verse(
        self, ctx: commands.Context, display_verse: Optional[StrictBool] = True, *, reference: str = "Joshua 21:8"
    ):
        """Returns a passage based off a reference"""
        version = self.users[ctx.author.id].preferred_version

        resp = await self.session.procget(reference, translation=version, verse_numbers=display_verse)
        url = f"https://biblegateway.com/passage/?search={resp.ref.replace(' ', '%20')}&version=NIV"

        if len(resp.text) > 1200:
            raise BibleError(f"Passage is too long.\nTry: <{url}>")

        footer = f"Translation: {resp.tr.name}"
        if version is None:
            footer += f" | If this version is difficult or this message too annoying, you can click the link or use {ctx.prefix}set_translation KJV"

        embed = Embed(title=resp.ref, description=resp.text, color=ctx.me.color, url=url).set_footer(text=footer)
        await ctx.send(embed=embed)

    @commands.command(aliases=["set_version", "translation", "version"])
    async def set_translation(self, ctx: commands.Context, *, translation: Optional[str]):
        """Sets a version to use in the bible_verse command
        Due to the limitations of the api I use (https://bible-api.com/),
        there's only a few functional translations (displayed by invoking
        the command)."""
        if isinstance(translation, str):
            translation = translation.strip().lower()

        if not translation:
            return await ctx.send(valid_translations_str)
        elif translation not in valid_translations:
            return await ctx.send("Invalid translation!\n" + valid_translations_str)

        self.users[ctx.author.id].preferred_version = translation
        self.bot.settings.save()
        translation = f"`{valid_translations[translation][0]}` [{valid_translations[translation][1]}]"
        await ctx.send(f"Set your translation to {translation}")


setup = Bible.basic_setup
