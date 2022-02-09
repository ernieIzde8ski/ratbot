import asyncio
import json
from logging import INFO, basicConfig, info
from typing import Any

import aiohttp

from utils.setup import Path, add_fn, ask_for_auth, fetch_one, fetch_up_to, fns, from_url, save


def prompt_continue(path: Path, msg: str = "Path {path} already exists. Continue anyways? ") -> bool:
    return input(msg.format(path=path.as_posix())).lstrip()[:1] in ("y", "Y", "1")


### Login credentials.
@add_fn
async def env_setup(*args, path: Path = Path("./.env"), **kwargs) -> None:
    """Setting login credentials."""
    if path.exists() and not prompt_continue(path):
        return info(f"Skipping file {path.as_posix()}")
    resp = ask_for_auth()
    save("./.env", resp)


### Defaults.
@add_fn
async def save_defaults(*args, **kwargs) -> None:
    """Saving default objects..."""
    with open("./utils/JSON/defaults.json", "r", encoding="utf-8") as file:
        defaults: dict[str, Any] = json.load(file)
    ignore_exists: bool | None = None
    for path, obj in defaults.items():
        path = Path(f"./data/{path}.json")
        if path.exists():
            if ignore_exists is None:
                ignore_exists = prompt_continue(
                    path, "Path {path} already exists. Continue anyways? (reusing setting) "
                )
            if not ignore_exists:
                info(f"Skipping file {path.as_posix()}")
                continue
            else:
                info(f"Replacing file {path.as_posix()}")
        save(path, json.dumps(obj, indent=2))


### Russian Bible.
@add_fn
async def generate_bible(
    *args, session: aiohttp.ClientSession, path: Path = Path("./data/russian.json"), **kwargs
) -> None:
    """Generating a Russian bible..."""
    if path.exists() and not prompt_continue(path):
        return info(f"Skipping file {path.as_posix()}")
    bible = await from_url(session)
    save(path, json.dumps(bible))


@add_fn
async def generate_xkcds(
    *args, session: aiohttp.ClientSession, path: Path = Path("./data/xkcd.json"), **kwargs
) -> None:
    """Generating XKCDs..."""
    if path.exists() and not prompt_continue(path):
        return info(f"Skipping file {path.as_posix()}")
    max = (await fetch_one(session))["int"]
    print(f"Going up to XKCD #{max}")
    res = await fetch_up_to(max, session)
    save("./data/xkcd.json", json.dumps(res))


async def main() -> None:
    Path("./data").resolve().mkdir(exist_ok=True)
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
    basicConfig(level=INFO)
    # For whatever reason, normal asyncio.run raises a superficial (as it works perfectly) RuntimeError
    # at the end of the process. This is a working workaround.
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(main())
