import asyncio
from functools import cached_property
import json
import logging
import random
from pathlib import Path
from typing import TYPE_CHECKING, Any, Generic, TypeVar

import pydantic
from discord import Message, TextChannel
from discord.ext import commands

if TYPE_CHECKING:
    from utils import RatBot

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


def generate_extensions_list(dir: Path = root / "cogs", suffix="cogs") -> list[str]:
    """Iterate through cogs directory and return a series of paths to Python files, formatted for `__import__`."""
    resp = []
    for path in dir.iterdir():
        if path.name == "__pycache__":
            continue
        elif path.is_file() and path.suffix.lower() == ".py":
            resp.append(f"{suffix}.{path.name.removesuffix(path.suffix)}")
        elif path.is_dir():
            resp.extend(generate_extensions_list(path, f"{suffix}.{path.name}"))
    return resp


class RatEmojis(pydantic.BaseModel):
    online: str = "<:online:708885917133176932>"
    offline: str = "<:offline:708886391672537139>"
    restart: str = "<:restarting:708887315853869087>"


class Settings(Saveable):
    _path = root / "settings.json"

    blocked: set[int] = pydantic.Field(default_factory=set)
    """IDs of users to ignore messages from."""
    default_prefixes: tuple[str, ...] = ("r.", "r!")
    """Default command prefixes. Can be overridden with the `prefix` command per guild."""
    emojis: RatEmojis = pydantic.Field(default_factory=RatEmojis)
    ratlord: int = 1014515185618255883
    """Role to mention when critical error logs occur."""

    @cached_property
    def pinglord(self):
        return f""

    guild_invite: str = "https://discord.gg/cdhrdaddyN"
    """Invite link to a guild."""
    github_repo: str = "https://github.com/ernieIzde8ski/ratbot/tree/v3"
    """Repository of this bot or the current branch of this bot."""
    music: list[str] = ["dQw4w9WgXcQ", "-FGrYI8XgPU"]
    """YouTube video keys, preferably of music."""

    debug: bool = True
    """Whether or not debugging is currently active."""
    enabled_extensions: list[str] = pydantic.Field(
        default_factory=generate_extensions_list
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

    class Config:
        # arbitrary_types_allowed = True
        keep_untouched = (cached_property,)


class DelayedLoad:
    _loaded = False
    """Whether the DelayedLoad instance has been loaded yet."""
    sleepytime: int | float = 2
    """Period waited in wait_until_loaded method."""

    async def wait_until_loaded(self):
        while self._loaded is False:
            await asyncio.sleep(self.sleepytime)

    async def update(self, bot: "RatBot"):
        """Method where class gets loaded. Set ._loaded to True in subclasses."""
        raise NotImplementedError(
            f"Method update is not implemented on subclass {type(self)}"
        )


class Channels(DelayedLoad, Saveable):
    _path = root / "settings.channels.json"

    class _Store(pydantic.BaseModel):
        status: int = 708882977202896957
        messages: int = 715297562613121084
        errors: int = 1014170368140922901
        based_meter: int = 762166605458964510
        guilds: int = 841863106996338699

    store: _Store = pydantic.Field(default_factory=_Store)

    async def set_channels(self, bot: "RatBot"):
        await bot.wait_until_ready()

        self.status: TextChannel
        """Channel to log on/off messages."""
        self.messages: TextChannel
        """Channel to log direct messages."""
        self.errors: TextChannel
        """Channel to log instances of CommandError."""
        self.based_meter: TextChannel
        """Channel to log new items from the based_meter command."""
        self.guilds: TextChannel
        """Channel to log guild join/leave events."""

        for name, id in dict(self.store).items():
            channel = bot.get_channel(id)
            if not channel:
                logging.error(f"Channel {name} with ID {id} not found")
            else:
                setattr(self, name, channel)

        self._loaded = True

        logging.info("Finished loading channels !")

    def save(self):
        raise NotImplementedError

    class Config:
        extra = pydantic.Extra.allow


settings = Settings.load()
channels = Channels.load()
