import re
from functools import partial
from typing import TypeVar

from disnake.ext.commands import Param

from lib.bot import Interaction

T = TypeVar("T")
_comma_pattern = re.compile(r"\s*(?<![^\\]\\),\s*")


def to_comma_list(_: Interaction, __s: str) -> list[str]:
    return re.split(_comma_pattern, __s)


CommaList = partial(Param, lambda _: list(), converter=to_comma_list)
