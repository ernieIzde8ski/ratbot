from typing import TypeVar

from .auth import ask_for_auth
from .russian import Bible
from .russian import from_url
from .XKCD import XKCD, XKCDum, fetch_one, fetch_up_to

fns = []
F = TypeVar("F")


def add_fn(fn: F) -> F:
    fns.append(fn)
    return fn


def save(path: str, obj: str) -> int:
    with open(path, "w+", encoding="utf-8") as file:
        return file.write(obj)
