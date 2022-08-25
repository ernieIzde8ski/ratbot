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
    """A model that can be saved to the path at `cls._path`."""

    indent: int | None = None
    "Indent level to save .json file at."
    _path = root
    "Path to load/save from."

    @classmethod
    def load(cls, path: Path | None = None, generate_when_missing=True):
        """Load the class from a json file."""
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
        """Save the class to a json file. Accepts extra params for cls.json"""
        indent = json_kwargs.pop("indent", self.indent)
        text = self.json(indent=indent, **json_kwargs)
        return (path or self._path).write_text(text)


def _enabled_extensions_factory(dir: Path = root / "cogs", suffix="cogs") -> list[str]:
    """Iterate through cogs directory and return a series of paths to Python files, formatted for `__import__`."""
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
    """IDs of users to ignore messages from."""
    default_prefixes: tuple[str, ...] = ("r.", "r!")
    """Default command prefixes. Can be overridden with the `prefix` command per guild."""

    guild_invite: str = "https://discord.gg/cdhrdaddyN"
    """Invite link to a guild."""
    github_repo: str = "https://github.com/ernieIzde8ski/ratbot/tree/v3"
    """Repository of this bot or the current branch of this bot."""
    music: list[str] = ["dQw4w9WgXcQ", "-FGrYI8XgPU"]
    """YouTube video keys, preferably of music."""

    enabled_extensions: list[str] = pydantic.Field(
        default_factory=_enabled_extensions_factory
    )
    """Extensions to set up while starting the bot."""

    custom_prefixes: dict[int, str] = pydantic.Field(default_factory=dict)
    """Mapping of [guild.id, prefix] set in `prefix` command."""

    @property
    def random_music(self):
        return f"https://youtu.be{random.choice(self.music)}"

    def get_prefix(self, bot: "RatBot", msg: Message) -> list[str]:
        if not msg.guild or msg.guild.id not in self.custom_prefixes:
            return commands.when_mentioned_or(*self.default_prefixes)(bot, msg)
        return commands.when_mentioned_or(self.custom_prefixes[msg.guild.id])(bot, msg)

    def reduce_enabled_extensions(self) -> None:
        "Sort and eliminate duplicate enabled extensions"
        self.enabled_extensions = sorted(set(self.enabled_extensions))


settings = Settings.load()
