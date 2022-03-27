from collections import defaultdict
from functools import cache, partial
from pathlib import Path
from typing import Any, Iterable, Literal, TypeVar

from pydantic import BaseModel, Field

from .functions import safe_load

T = TypeVar("T")


class SaveableModel(BaseModel):
    """Model that exists for the purpose of subclassing further."""

    path: str
    """Path to a saved instance of the model."""

    @classmethod
    def load(cls, path: str, default_kwargs: Any = ...):
        """Loads the class from its filepath or a given one."""
        path = path or cls.path
        kwargs = safe_load(path, default_kwargs)
        return cls(path=path, **kwargs)

    def save(self, mode="w+", *__additional_exclusions: str) -> int:
        """Saves the current model to the path, returning the operation's exit code."""
        json = self.json(exclude={"path", *__additional_exclusions})
        with open(self.path, mode, encoding="utf-8") as file:
            return file.write(json)


class RepresentableModel(BaseModel):
    @staticmethod
    def __str_item(__k: str, __v: Any):
        return f"""{__k}: {f"'{__v}'" if isinstance(__v, str) else __v}"""

    def __str__(self) -> str:
        return "\n".join(self.__str_item(k, v) for k, v in self)


## data/settings.json


class RatEmojis(BaseModel):
    power_on: str = "🐣"
    power_off: str = "🎃"
    laugh: str = "🤬"
    trolls: list[str] = ["🧌"]


class RatGuildConfigs(BaseModel):
    ban_chance: float | None = None
    """Chance of being banned on a random message. None if not enabled."""
    pipi_enabled: bool = True
    """Whether or not to inflict members of the guild with the Petrosian copypasta. Defaults to yes."""


class RatUserConfigs(BaseModel):
    preferred_version: str | None = None
    """Preferred Bible translation"""
    tz: str | None = None
    """Timezone"""


class RatSettings(SaveableModel):
    """Settings loaded in from data/settings.json"""

    songs: dict[str, str] = {}
    """Dictionary of songs, mapped Key:Title"""
    emojis: RatEmojis = Field(default_factory=RatEmojis)
    """Emojis used in various commands and responses"""
    guilds: defaultdict[int, RatGuildConfigs] = Field(default_factory=partial(defaultdict, RatGuildConfigs))
    """Per-guild configurations"""
    users: defaultdict[int, RatUserConfigs] = Field(default_factory=partial(defaultdict, RatUserConfigs))
    """Per-user configurations"""
    measured: set[str] = Field(default_factory=set)
    """Set of based_meter arguments that have already been processed."""


## config.json


def _get_all_cogs(cog_dir: Path):
    cog_dir = cog_dir.absolute()
    posix = cog_dir.as_posix()

    def fix(p: Path):
        """Turns a filepath into something importable from the project directory"""
        # Remove the first part of the filepath, then the leading slash/trailing suffix, and finally coerce into import format
        resp = p.as_posix().removeprefix(posix)
        resp = resp[1:-3]
        return "cogs." + resp.replace("/", ".")

    for p0 in cog_dir.iterdir():
        if p0.is_dir():
            for p1 in p0.iterdir():
                if not p1.is_dir() and p1.suffix == ".py":
                    yield fix(p1)
        elif p0.suffix == ".py":
            yield fix(p0)


def get_all_cogs(cog_dir: Path = Path("./cogs")) -> set[str]:
    return set(_get_all_cogs(cog_dir))


class config_channels(BaseModel):
    __all__ = ("BM", "DM", "Status", "Guilds")
    BM: int = 762166605458964510
    """For dumping new based_meter arguments into"""
    DM: int = 715297562613121084
    """For handling direct messages to the bot"""
    Status: int = 708882977202896957
    """For handling on/off messages"""
    Guilds: int = 841863106996338699
    """For notifying of guilds joined and left"""

    def items(self) -> Iterable[tuple[str, int]]:
        for attr in self.__all__:
            yield attr, getattr(self, attr)


class RatConfig(SaveableModel):
    """Config from config.json"""

    prefix: list[str] = ["r.", "r!"]
    """Default bot prefix"""
    status: str = "{}help"
    """Default status to load. {} params will be replaced with prefix."""
    tz: str = "EST"
    """Default timezone, PYTZ compatible. I'm not quite sure where this is used anymore."""
    github: str = "https://github.com/ernieIzde8ski/ratbot"
    """URL to the bot's repo."""
    primary_guild: int = 488475203303768065
    """ID of the bot owner's guild."""
    invite: str = "https://discord.gg/3gfP2kYPp4"
    """Invite to the primary guild."""
    channels: config_channels = Field(default_factory=config_channels)
    """IDs of various channels inside the primary guild."""
    enabled_extensions: set[str] = Field(default_factory=get_all_cogs)
    """Extensions to load on startup."""


## Weather Classes

RawUnits = Literal["standard", "metric", "imperial"]


class WUserCoords(BaseModel):
    """Some issues occurred with NamedTuple and I stopped thinking about it"""

    lat: float = 0.0
    lon: float = 0.0

    def __iter__(self):
        yield self.lat
        yield self.lon


class WUser(RepresentableModel):
    coords: WUserCoords | None = None
    units: RawUnits = "standard"
    guild_id: int = 488475203303768065
    """The API gives you multiple servers when a user switches their status. This changes it to just 1."""
    tz: str = "America/Los_Angeles"
    last_sent: str = "0000-00-00"
    aliases: list[str] = ["Bozo"]


class WUsers(BaseModel):
    active: set[int] = Field(default_factory=set)
    """Set of users to send the daily message to"""
    all: defaultdict[int, WUser] = Field(default_factory=partial(defaultdict, WUser))
    """User data"""


class RatWeatherResponses(BaseModel):
    greetings: list[str] = Field(default_factory=list)
    """First part of the daily weather notification. Each greeting includes {} for formatting."""
    temp_reactions: list[tuple[int, str]] = Field(default_factory=list)
    """Reactions to the current temperature, mapped as Kelvin/Reaction. Bot checks lower bounds first."""
    final_reaction: str = "You will die"
    """Reaction when temp_reactions are exhausted"""
    music_ignored: str = "WHAT IS WRONG WTIH YOU ARE YOU STUPID AOR SOMETHING . OR ARE YOU JUST STUPID OR ARE YOU"
    """Reaction when the prompt for music is ignored"""
    music_approved: list[str] = ["Awsom", "Based", "Yes", "Yea", "Good", "Here"]
    """Reactions when the prompt for music is accepted"""
    music_rejected: list[str] = ["Rude", "Dam", "Cringe ?", "Troled", '"You Will Die" -- Helloween guy']
    """Reactions when the prompt for music is rejected"""


class RatWeatherData(SaveableModel):
    """Data from data/weather.json"""

    users: WUsers = Field(default_factory=WUsers)
    """User data on location/unit preferences"""
    resps: RatWeatherResponses = Field(default_factory=RatWeatherResponses)
    """Things to say to people"""
    music_chance: float = 0.10
    """Chance for rat to ask to recommend music"""
