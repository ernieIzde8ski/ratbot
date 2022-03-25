from collections import defaultdict
from functools import partial
from typing import Literal, NamedTuple

from pydantic import BaseModel, Field


class SaveableModel(BaseModel):
    """Model that exists for the purpose of subclassing further."""

    path: str
    """Path to a saved instance of the model."""

    def save(self, mode="w+", *__additional_exclusions: str) -> int:
        """Saves the current model to the path, returning the operation's exit code."""
        json = self.json(exclude={"path", *__additional_exclusions})
        with open(self.path, mode, encoding="utf-8") as file:
            return file.write(json)


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


class RatConfigChannels(BaseModel):
    BM: int = 762166605458964510
    """For dumping new based_meter arguments into"""
    DM: int = 715297562613121084
    """For handling direct messages to the bot"""
    Status: int = 708882977202896957
    """For handling on/off messages"""
    Guilds: int = 841863106996338699
    """For notifying of guilds joined and left"""


class RatConfig(SaveableModel):
    """Config from config.json"""

    prefix: list[str] = ["r.", "r!"]
    """Bot prefix"""
    status: str = "{}help"
    """Default status to load"""
    tz: str = "EST"
    """Default timezone, PYTZ compatible. I'm not quite sure where this is used anymore."""
    github: str = "https://github.com/ernieIzde8ski/ratbot"
    """URL to the bot's repo."""
    primary_guild: int = 488475203303768065
    """ID of the bot owner's guild."""
    invite: str = "https://discord.gg/3gfP2kYPp4"
    """Invite to the primary guild."""
    channels: RatConfigChannels = Field(default_factory=RatConfigChannels)
    """IDs of various channels inside the primary guild."""


## Weather Classes

RawUnits = Literal["standard", "metric", "imperial"]


class NamedCoords(BaseModel):
    """Some issues occurred with NamedTuple and I stopped thinking about it"""

    lat: float = 0.0
    lon: float = 0.0

    def __iter__(self):
        yield self.lat
        yield self.lon


class WUser(BaseModel):
    coords: NamedCoords = Field(default_factory=NamedCoords)
    units: RawUnits = "metric"
    guild_id: int = 488475203303768065
    tz: str = "GMT"
    last_sent: int = 0
    aliases: set[str] = {"Bozo"}


class WUsers(BaseModel):
    active: set[int] = Field(default_factory=set)
    """Set of users to send the daily message to"""
    all: defaultdict[int, WUser] = Field(default_factory=partial(defaultdict, WUser))
    """User data"""


class RatWeatherResponses(BaseModel):
    greetings: set[str] = Field(default_factory=set)
    """First part of the daily weather notification. Includes {} for formatting."""
    temp_reactions: list[tuple[int, str]] = Field(default_factory=list)
    """Reactions to the current temperature, mapped as Kelvin/Reaction. Bot checks lower bounds first."""
    final_reaction: str = "You will die"
    """Reaction when temp_reactions are exhausted"""


class RatWeatherData(SaveableModel):
    """Data from data/weather.json"""

    users: WUsers = Field(default_factory=WUsers)
    """User data on location/unit preferences"""
    resps: RatWeatherResponses = Field(default_factory=RatWeatherResponses)
    """Things to say to people"""
