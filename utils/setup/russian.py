from json import loads
from typing import TypedDict
import random

import aiohttp


URL = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ru_synodal.json"


BibleVerse = list[str]


class BibleBook(TypedDict):
    abbrev: str
    chapters: list[BibleVerse]
    name: str


Bible = list[BibleBook]


def converter(bible: Bible) -> list[str]:
    resp = []
    for book in bible:
        for chapter in book["chapters"]:
            for verse in chapter:
                resp.append(verse)
    # I'm not really gonna need the *whole* bible.
    resp = random.sample(resp, 10000)
    return resp


async def from_url(session: aiohttp.ClientSession, url: str = URL) -> list[str]:
    """Returns a bible from the URL."""
    async with session.get(url) as res:
        res = await res.content.read()
        return converter(loads(res))
