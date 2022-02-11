import json
from typing import Any


def strip_str(text: str) -> str:
    """Strips away much of a string

    In order, this function removes non-ASCII, removes
    characters duplicated more than twice, lowercases
    the string, and removes whitespace.
    """
    text = "".join([c for c in text if ord(c) <= 128])
    resp = "  "
    for i in text:
        if i == resp[-1] and i == resp[-2]:
            continue
        else:
            resp += i
    resp = "".join(resp.lower().split())
    return resp


def safe_load(fp: str, backup: Any = None) -> Any:
    """Load a file & create it from the backup variable if it doesn't exist"""
    try:
        with open(fp, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError as err:
        if backup is None:
            raise err from err
        with open(fp, "x", encoding="utf-8") as file:
            json.dump(backup, file)
            return backup


def safe_dump(fp: str, obj: Any) -> None:
    """Write to a file & create it if it doesn't exist"""
    with open(fp, "w+", encoding="utf-8") as file:
        json.dump(obj, file)
