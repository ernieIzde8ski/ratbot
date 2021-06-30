from typing import Any
import json


def safe_load(fp: str, backup) -> Any:
    """Load a file & create it from the backup variable if it doesn't exist"""
    try:
        with open(fp, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        with open(fp, "x", encoding="utf-8") as file:
            json.dump(backup, file)
            return backup


def safe_dump(fp: str, obj) -> None:
    """Write to a file & create it if it doesn't exist"""
    try:
        with open(fp, "w", encoding="utf-8") as file:
            json.dump(obj, file)
    except FileNotFoundError:
        with open(fp, "x", encoding="utf-8") as file:
            json.dump(obj, file)
