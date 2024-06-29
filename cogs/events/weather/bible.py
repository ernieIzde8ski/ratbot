import json
import logging
from typing import TypedDict

from aiohttp import ClientSession

from lib import dirs

_bible_url = r"https://raw.githubusercontent.com/thiagobodruk/bible/49a869c278bcd91ced78a5d64fe2d92ac812e2ca/json/ru_synodal.json"


class Book(TypedDict):
    abbrev: str
    chapters: list[list[str]]
    name: str


async def getch_bible(session: ClientSession) -> list[str]:
    """
    Gets the Russian Synodal Bible from ~/.local/share/bible.json,
    or fetches it from the internet if it hasn't been downloaded yet.
    """
    bible_path = dirs.data_home() / "bible.json"
    if bible_path.exists():
        with open(bible_path, "r") as file:
            return json.load(file)

    logging.debug("Downloading Russian Synodal Bible...")
    async with session.get(_bible_url) as resp:
        text = (await resp.read()).decode("utf-8-sig")
        the_holy_bible: list[Book] = json.loads(text)

    logging.debug("Parsing the Bible...")
    verses = []
    for book in the_holy_bible:
        for chapter in book["chapters"]:
            verses.extend(chapter)

    logging.debug("Saving the Bible...")
    bible_path.parent.mkdir(exist_ok=True)
    with open(bible_path, "w") as file:
        json.dump(verses, file)

    logging.debug("Bible acquired!")
    return verses
