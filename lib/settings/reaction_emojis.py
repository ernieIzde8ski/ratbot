import re
from typing import Self

from pydantic import BaseModel


class ReactionEmojis(BaseModel):
    trigger: re.Pattern
    reactions: list[str]
    chance: float = 0.20

    @classmethod
    def default(cls) -> Self:
        return cls(trigger=re.compile(r"(?i)trol[eli]"), reactions=["🧌"])
