import re
from typing import Pattern, TypedDict, Union

import discord
from discord.ext import commands
from discord.message import Message

from utils.functions import safe_dump, safe_load
from ._types import WeatherUsers
from utils.weather_retrieval import WeatherRetrieval


class RatConfig(TypedDict):
    prefix: list[str]
    default_status: str
    preferred_timezone: str
    github: str
    invite: str
    primary_guild: str
    channels: dict[str, Union[int, discord.TextChannel]]


class StatusChannels:
    BM: discord.TextChannel
    DM: discord.TextChannel
    Status: discord.TextChannel
    Guilds: discord.TextChannel

    def __init__(self, **channels: dict[str, int]):
        self.channels = channels
        self.loaded = False

    def get_channels(self, bot) -> None:
        """Retrieve channels for later usage"""
        for k, v in self.channels.items():
            c = bot.get_channel(v)
            if c is None:
                print(f"Could not get channel {k} from id {v}")
            setattr(self, k, c)
        self.loaded = True


class Blocking:
    def __init__(self):
        self.blocked: list[int] = safe_load("data/blocked.json", [])

    def set_blocked(self, blocked: list[int]) -> None:
        self.blocked = blocked

    def update_blocked(self, blockee: discord.User | discord.Member) -> None:
        self.blocked.append(blockee.id)
        safe_dump("data/blocked.json", self.blocked)

    def unblock(self, blockee: discord.User | discord.Member) -> None:
        self.blocked.remove(blockee.id)
        safe_dump("data/blocked.json", self.blocked)

    async def reply(self, message: discord.Message) -> bool:
        """Returns whether or not a message is good for command parsing"""
        if message.author.bot:
            return False
        elif message.guild:
            if message.channel.name == "rat" and (message.content != "rat" or message.attachments):
                await message.delete()
                return False

        if message.author.id in self.blocked:
            return False

        elif "rat" in message.content.split():
            await message.channel.send("rat")
        return True


class Prefixes:
    def __init__(self, default_prefix: list[str]):
        self.prefix = default_prefix
        self.prefixes: dict[str, str] = safe_load("data/prefixes.json", {})

    async def get(self, bot: commands.Bot, message: discord.Message) -> list:
        """Return a prefix off of context"""
        if message.guild is None:
            return commands.when_mentioned(bot, message) + self.prefix + [""]
        prefix = self.prefixes.get(str(message.guild.id))
        if prefix is None:
            return commands.when_mentioned(bot, message) + self.prefix
        else:
            return commands.when_mentioned_or(prefix)(bot, message)

    async def update(self, id: str, new_prefix: str) -> None:
        """Update a guild's prefix"""
        self.prefixes[id] = new_prefix
        safe_dump("data/prefixes.json", self.prefixes)

    async def reset(self, id: str) -> None:
        """Reset a guild's prefix"""
        self.prefixes.pop(id)


class Weather(WeatherRetrieval):
    def __init__(self, apikey: str, *, locations_fp: str = "data/weather_locations.json") -> None:
        super().__init__(apikey)
        self.locs: WeatherUsers = safe_load(locations_fp, {})

    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.apikey}]"

    def save(self, *, locations_fp: str = "data/weather_locations.json") -> None:
        safe_dump(locations_fp, self.locs)


class RatData:
    def __init__(
        self,
        *,
        banning_guilds_fp: str = "data/banning.json",
        pipi_guilds_fp: str = "data/pipi.json",
        tenor_guilds_fp: str = "data/tenor_guilds.json",
        songs_fp: str = "data/songs.json",
        trollgex_fp: str = "data/trollgex.json",
        trolljis_fp: str = "data/trolls.json",
    ) -> None:
        self.weather_loaded = False
        self.banning_guilds: dict = safe_load(banning_guilds_fp, {})
        self.pipi_guilds: set[str] = set(safe_load(pipi_guilds_fp, []))
        self.tenor_guilds: set[int] = set(safe_load(tenor_guilds_fp, []))
        self.songs: list[str] = safe_load(songs_fp, [])
        self.trollgex: Pattern[str] = re.compile(safe_load(trollgex_fp, "(?i)troll"))
        self.trolljis: list[str] = safe_load(trolljis_fp, [])
        self.msg: Message | None = None

    def load_weather_configs(
        self,
        *,
        bible_fp: str = "data/russian.json",
        resps_fp: str = "data/weather_resps.json",
        users_fp: str = "data/weather_users.json",
    ) -> None:
        self.bible: list = safe_load(bible_fp, [])
        self.resps: dict = safe_load(resps_fp, {})
        self.users: WeatherUsers = safe_load(users_fp, {"active_users": []})


class RatBot(commands.Bot):
    def __init__(self, *args, config: RatConfig, block_check: Blocking, **kwargs):
        self.pfx = Prefixes(config["prefix"])
        super().__init__(*args, command_prefix=self.pfx.get, **kwargs)

        self.config = config
        self.data = RatData()
        self.status_channels = StatusChannels(**config["channels"])
        self.block_check = block_check

        self.loop.create_task(self.on_complete())

    async def on_complete(self) -> None:
        await self.wait_until_ready()
        self.app = await self.application_info()
        print(f"Retrieved application info! (owner: {self.app.owner})")

    def load_weather(self, apikey: str | None) -> None:
        if getattr(self, "weather", None) is not None:
            print("Ignoring attempt to reload weather class")
        elif apikey is None:
            raise ValueError("Apikey must have a value")
        else:
            self.weather = Weather(apikey)
