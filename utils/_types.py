from typing import Any, Type, TypedDict
from typing_extensions import NotRequired

Bible = dict[str, str]
""" A dictionary mapping member ID to translation. Corresponds to bible.json. """

Russian = list[str]
""" A list of bible verses. Corresponds to russian.json. """
