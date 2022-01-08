import asyncio
import json
from typing import Any

import aiohttp

from utils.setup import *


### Login credentials.
@add_fn
async def env_setup(*args, **kwargs) -> None:
    """Setting login credentials."""
    resp = ask_for_auth()
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
    bible = await from_url(session)
    save("./data/russian.json", json.dumps(bible))


@add_fn
async def generate_xkcds(*args, session: aiohttp.ClientSession, **kwargs) -> None:
    """Generating XKCDs..."""
    max = (await fetch_one(session))["int"]
    print(f"Going up to XKCD #{max}")
    res = await fetch_up_to(max, session)
    save("./data/xkcd.json", json.dumps(res))


async def main() -> None:
    session = aiohttp.ClientSession()
    errs: list[str] = []
    sucs: list[str] = []
    for fn in fns:
        print(fn.__doc__)
        try:
            await fn(session=session)
        except Exception as err:
            print(f"{err.__class__.__name__}: {err}")
            errs.append(fn.__name__)
        else:
            sucs.append(fn.__name__)
            print("Done!")
    if errs:
        print("Errors occurred on:", ", ".join(errs))
        print("The following functions succeeded:", ", ".join(sucs))
    await session.close()


if __name__ == "__main__":
    # For whatever reason, normal asyncio.run raises a superficial (as it works perfectly) RuntimeError
    # at the end of the process. This is a working workaround.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
