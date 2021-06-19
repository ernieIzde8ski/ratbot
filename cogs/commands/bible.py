from textwrap import fill
from aiohttp import ClientSession
from discord.ext import commands
from json import load, dump
from discord import Embed


class Bible(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        try:
            with open("data/bible.json", "r") as file:
                self.data = load(file)
        except FileNotFoundError:
            self.data = {}
            with open("data/bible.json", "x") as file:
                dump(self.data, file)

    @staticmethod
    async def get_text(reference, characters_per_line: int = 70) -> dict:
        async with ClientSession() as session:
            async with session.get(f"https://bible-api.com/{reference}") as resp:
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
    def embed_constructor(text: dict, color) -> Embed:
        url = "https://biblegateway.com/passage/?search={}&version=NIV"
        return Embed(
            title=text["reference"],
            description=text["content"],
            color=color,
            url=url.format(text["reference"].replace(" ", "%20"))
        ).set_footer(text=f"Translation: {text['translation']}")

    @commands.command(aliases=["v", "🙏"])
    async def bible_verse(self, ctx, *, reference: str = "Joshua 21:8"):
        """Returns a passage based off a reference"""
        text = await self.get_text(reference)

        if text.get("error"):
            return await ctx.send(f"error: {text['error']}")
        elif text["content"].__len__() > 1000:
            reference = text["reference"].replace(' ', "%20")
            return await ctx.send(f"error: passage is too long\ntry https://biblegateway.com/passage/?search={reference}")
        else:
            await ctx.send(embed=self.embed_constructor(text, ctx.me.color))


def setup(bot):
    bot.add_cog(Bible(bot))
