import json
import logging
import random
from pathlib import Path
from typing import TYPE_CHECKING

from discord import Message
from discord.ext import commands

if TYPE_CHECKING:
    from utils import RatBot

import pydantic

root = Path(__file__).parent


class Saveable(pydantic.BaseModel):
    indent: int | None = None
    _path = root

    @classmethod
    def load(cls, path: Path | None = None, generate_when_missing=True):
        path = (path or cls._path).absolute()
        try:
            return cls(**json.loads(path.read_text()))
        except FileNotFoundError:
            if not generate_when_missing:
                raise
            logging.error(f"No {cls.__name__} instance found at path: {path}")
            res = cls()
            res.save()
            return res

    def save(self, path: Path | None = None, **json_kwargs):
        indent = json_kwargs.pop("indent", self.indent)
        text = self.json(indent=indent, **json_kwargs)
        return (path or self._path).write_text(text)


def _enabled_extensions_factory(dir: Path = root / "cogs", suffix="cogs") -> list[str]:
    resp = []
    for path in dir.iterdir():
        if path.name == "__pycache__":
            continue
        elif path.is_file() and path.suffix.lower() == ".py":
            resp.append(f"{suffix}.{path.name.removesuffix(path.suffix)}")
        elif path.is_dir():
            resp.extend(_enabled_extensions_factory(path, f"{suffix}.{path.name}"))
    return resp


class Settings(Saveable):
    _path = root / "settings.json"

    blocked: set[int] = pydantic.Field(default_factory=set)
    default_prefixes: tuple[str, ...] = ("r.", "r!")

    guild_invite: str = "https://discord.gg/cdhrdaddyN"
    github_repo: str = "https://github.com/ernieIzde8ski/ratbot/tree/v3"
    music: list[str] = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=-FGrYI8XgPU",
    ]

    enabled_extensions: list[str] = pydantic.Field(
        default_factory=_enabled_extensions_factory
    )
    custom_prefixes: dict[int, str] = pydantic.Field(default_factory=dict)

    @property
    def random_music(self):
        return random.choice(self.music)

    def get_prefix(self, bot: "RatBot", msg: Message) -> list[str]:
        if not msg.guild or msg.guild.id not in self.custom_prefixes:
            return commands.when_mentioned_or(*self.default_prefixes)(bot, msg)
        return commands.when_mentioned_or(self.custom_prefixes[msg.guild.id])(bot, msg)

    def reduce_enabled_extensions(self) -> None:
        "Sort and eliminate duplicate enabled extensions"
        self.enabled_extensions = sorted(set(self.enabled_extensions))


settings = Settings.load()
