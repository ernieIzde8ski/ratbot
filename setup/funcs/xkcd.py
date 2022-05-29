import json
import logging
from typing import TypedDict
from urllib.request import urlopen

from .generics import data, register_func

base_url = "https://xkcd.com"
default_url = f"{base_url}/info.0.json"


class Comic(TypedDict):
    month: str
    num: int
    link: str
    year: str
    news: str
    safe_title: str
    transcript: str
    alt: str
    img: str
    title: str
    day: str


class CachedComic(TypedDict):
    name: str
    alt: str
    int: int


def fetch_xkcd(n: int = ...) -> Comic:
    url = default_url if n is ... else f"{base_url}/{n}/info.0.json"
    with urlopen(url) as res:
        text = res.read().decode(res.headers.get_content_charset() or "utf-8")
        return json.loads(text)


@register_func
def generate_xkcds():
    """Assembling XKCD cache..."""
    path = data / "xkcd.json"
    if path.exists():
        cont = input("An xkcd cache already exists. Continue anyways? [y/N]")[:1]
        if cont.lower() != "y":
            return

    max = fetch_xkcd()["num"]
    logging.debug(f"XKCD: Going up to #{max}")
    xkcds = ((fetch_xkcd(n)) for n in range(1, max + 1) if n != 404)
    resp: list[CachedComic] = []

    for xkcd in xkcds:
        comic = CachedComic(name=xkcd["safe_title"], alt=xkcd["alt"], int=xkcd["num"])
        resp.append(comic)
        if comic["int"] % 50:
            logging.info(f"XKCD: #{str(comic['int']).zfill(4)} - '{comic['name']}'")

    with open(path, "w+"):
        json.dumps(resp)
