import json
from pathlib import Path
from typing import Callable, TypeVar

funcs: list[Callable] = []

setup = Path("setup")
data = Path("data")
if not data.exists():
    data.mkdir()


class InputError(ValueError):
    pass


T = TypeVar("T")


def register_func(func: Callable[[], T], /) -> Callable[[], T]:
    funcs.append(func)
    return func


@register_func
def create_generics():
    path = setup / "funcs" / "generics.json"
    with open(path, "r") as file:
        generics: dict = json.load(file)
    for k, v in generics.items():
        with open(data / f"{k}.json", "w") as file:
            json.dump(v, file)
