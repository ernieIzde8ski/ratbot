import asyncio
import aiohttp
import json
from typing import Any, TypeVar, TypedDict


fns = []
F = TypeVar("F")


def add_fn(fn: F) -> F:
    fns.append(fn)
    return fn


def save(path: str, obj: str) -> int:
    with open(path, "w+", encoding="utf-8") as file:
        return file.write(obj)


### Login credentials.
@add_fn
async def env_setup(*args, **kwargs) -> None:
    """Setting login credentials."""
    print("Setting .env variables. Make sure you have a token from")
    print("https://discord.com/developers (required) && an API key from")
    print("https://openweathermap.org/api (optional).")
    token = input("Token?   ")
    apikey = input("API key? ")
    if not token:
        raise KeyError("Expected token.")
    resp = f"DISCORD_TOKEN = {token}\n"
    if not apikey:
        print("Remember to disable the weather cogs!")
    else:
        resp += f"WEATHER_TOKEN = {apikey}\n"
    save("./.env", resp)


### Defaults.
@add_fn
async def save_defaults(*args, **kwargs) -> None:
    """Saving default objects..."""
    with open("./utils/JSON/defaults.json", "r", encoding="utf-8") as file:
        defaults: dict[str, Any] = json.load(file)
    for path, obj in defaults.items():
        save(f"./data/{path}.json", json.dumps(obj, indent=2))


### Russian Bible.
@add_fn
async def generate_bible(*args, session: aiohttp.ClientSession, **kwargs) -> None:
    """Generating a Russian bible..."""
    from utils.russian import converter, URL

    async with session.get(URL) as res:
        res = await res.content.read()
        bible = converter(json.loads(res))
        save("./data/russian.json", json.dumps(bible))


### XKCDs.
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


async def fetch_xkcd(session: aiohttp.ClientSession, i: int = None) -> XKCDum:
    url = XKCD_URL.format(NUM=i or "")
    async with session.get(url) as result:
        resp: XKCD = json.loads(await result.content.read())
        return XKCDum(name=resp["safe_title"], alt=resp["alt"], int=resp["num"])


@add_fn
async def generate_xkcds(*args, session: aiohttp.ClientSession, **kwargs) -> None:
    """Generating XKCDs..."""
    resp: list[XKCDum] = []
    max = (await fetch_xkcd(session))["int"]
    print(f"Going up to XKCD #{max}")
    for i in range(1, max + 1):
        try:
            resp.append(await fetch_xkcd(session, i))
        except Exception as err:
            if i == 404:
                print(err.__class__.__name__, i)
            else:
                raise err
        if i % 50 == 0:
            print(resp[-1]["int"], resp[-1]["name"])
    save("./data/xkcd.json", json.dumps(resp))


async def main() -> None:
    session = aiohttp.ClientSession()
    errs: list[str] = []
    sucs: list[str] = []
    for fn in fns:
        print(fn.__doc__)
        try:
            await fn(session=session)
        except Exception as err:
            print(err)
            errs.append(fn.__name__)
        else:
            sucs.append(fn.__name__)
            print("Done!")
    await session.close()


if __name__ == "__main__":
    # For whatever reason, normal asyncio.run raises a superficial (as it works perfectly) RuntimeError
    # at the end of the process. This is a working workaround.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
