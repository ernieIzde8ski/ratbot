import random
import json
from typing import TypedDict
from .generics import register_func, data
from urllib.request import urlopen

synodal_bible = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ru_synodal.json"


class BibleBook(TypedDict):
    abbrev: str
    chapters: list[list[str]]
    name: str


def get_bible() -> list[BibleBook]:
    with urlopen(synodal_bible) as res:
        # magic encoding derived from trial & error
        text = res.read().decode("utf-8-sig")
        return json.loads(text)


@register_func
def russian_bible():
    verses = []
    for book in get_bible():
        for chapter in book["chapters"]:
            verses.extend(chapter)
    # I don't need the *whole* bible.
    # As it turns out, randomly joined sentences read like garbage regardless.
    verses = random.sample(verses, 10_000)
    path = data / "russian_bible.json"
    with open(path, "w+") as file:
        json.dump(verses, file)
