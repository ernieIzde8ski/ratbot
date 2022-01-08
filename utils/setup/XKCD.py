### XKCDs.
import json
from typing import TypedDict

import aiohttp


class XKCD(TypedDict):
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


class XKCDum(TypedDict):
    name: str
    alt: str
    int: int


XKCD_URL = "https://xkcd.com/{NUM}/info.0.json"


async def fetch_one(session: aiohttp.ClientSession, i: int = None) -> XKCDum:
    url = XKCD_URL.format(NUM=i or "")
    async with session.get(url) as result:
        resp: XKCD = json.loads(await result.content.read())
        return XKCDum(name=resp["safe_title"], alt=resp["alt"], int=resp["num"])

async def fetch_up_to(upper: int, session: aiohttp.ClientSession) -> list[XKCDum]:
    resp: list[XKCDum] = []
    for i in range(1, upper+1):
        try:
            resp.append(await fetch_one(session, i))
        except Exception as err:
            if i == 404:
                print(err.__class__.__name__, i)
            else:
                raise err
        if i % 50 == 0:
            print(resp[-1]["int"], resp[-1]["name"])
    return resp