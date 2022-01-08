import json
from pathlib import Path
from typing import TypedDict
import random


# Before I totally deprecate this, might as well make it absolute so my issues go away
PATH = (Path(__file__).parent / Path("../data/russian.json")).resolve()
URL = "https://raw.githubusercontent.com/thiagobodruk/bible/master/json/ru_synodal.json"


BibleVerse = list[str]


class BibleBook(TypedDict):
    abbrev: str
    chapters: list[BibleVerse]
    name: str


Bible = list[BibleBook]


def load() -> Bible:
    with open(PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def converter(bible: Bible) -> list[str]:
    resp = []
    for book in bible:
        for chapter in book["chapters"]:
            for verse in chapter:
                resp.append(verse)
    # I'm not really gonna need the *whole* bible.
    resp = random.sample(resp, 10000)
    return resp


def _main(bible: Bible = None) -> None:
    """Function called by main. Exists so that _main might use exception handling."""
    resp = converter(bible or load())
    with open(PATH, "w+", encoding="utf-8") as file:
        json.dump(resp, file)
    print("Converted Russian bible into proper format!")


def main(bible: Bible = None):
    try:
        _main()
    except TypeError:
        con = input("Bible has already been processed. Retry? [y/N] ")
        if con and con[0] in ("y", "Y", "1"):
            import requests

            bible = json.loads(requests.get(URL).content)
            _main(bible)


if __name__ == "__main__":
    main()
