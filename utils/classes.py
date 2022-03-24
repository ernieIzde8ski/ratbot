import re
from typing import Callable, Coroutine, Pattern, TypedDict, Union
import aiohttp

import discord
from discord.ext import commands
from discord.message import Message

from utils.functions import safe_dump, safe_load
from utils.openweathermap import RatWeather


class RatConfig(TypedDict):
    prefix: list[str]
    default_status: str
    preferred_timezone: str
    github: str
    invite: str
    primary_guild: int
    channels: dict[str, Union[int, discord.TextChannel]]


class StatusChannels:
    BM: discord.TextChannel
    DM: discord.TextChannel
    Status: discord.TextChannel
    Guilds: discord.TextChannel

    def __init__(self, **channels: dict[str, int]):
        self.channels = channels
        self.loaded = False

    def get_channels(self, bot: "RatBot") -> None:
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
        self.blocked.append(blockee.id)  # type: ignore
        safe_dump("data/blocked.json", self.blocked)

    def unblock(self, blockee: discord.User | discord.Member) -> None:
        self.blocked.remove(blockee.id)  # type: ignore
        safe_dump("data/blocked.json", self.blocked)

    async def reply(self, message: discord.Message) -> bool:
        """Returns whether or not a message is good for command parsing"""
        if message.author.bot:  # type: ignore
            return False
        elif message.guild:
            if message.channel.name == "rat" and (message.content != "rat" or message.attachments):
                await message.delete()
                return False

        if message.author.id in self.blocked:  # type: ignore
            return False

        elif "rat" in message.content.split():
            await message.channel.send("rat")
        return True


class Prefixes:
    def __init__(self, default_prefix: list[str]):
        self.prefix = default_prefix
        self.prefixes: dict[str, str] = safe_load("data/prefixes.json", {})

    async def get(self, bot: "RatBot", message: discord.Message) -> list:
        """Return a prefix off of context"""
        if message.guild is None:
            return commands.when_mentioned(bot, message) + self.prefix + [""]
        prefix = self.prefixes.get(str(message.guild.id))  # type: ignore
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


class RatData:
    def __init__(
        self,
        *,
        banning_guilds_fp: str = "data/banning.json",
        pipi_guilds_fp: str = "data/pipi.json",
        tenor_guilds_fp: str = "data/tenor_guilds.json",
        songs_fp: str = "data/songs.json",
        trolljis_fp: str = "data/trolls.json",
    ) -> None:
        self.banning_guilds: dict = safe_load(banning_guilds_fp, {})
        self.pipi_guilds: set[str] = set(safe_load(pipi_guilds_fp, []))
        self.tenor_guilds: set[int] = set(safe_load(tenor_guilds_fp, []))
        self.songs: list[str] = safe_load(songs_fp, [])
        self.trolljis: list[str] = safe_load(trolljis_fp, [])
        self.msg: Message | None = None


class RatBot(commands.Bot):
    weather: RatWeather
    weather_apikey: str | None

    def __init__(self, *args, config: RatConfig, block_check: Blocking, weather_apikey: str | None = None, **kwargs):
        self.pfx = Prefixes(config["prefix"])
        super().__init__(*args, command_prefix=self.pfx.get, **kwargs)

        self.config = config
        self.data = RatData()
        self.status_channels = StatusChannels(**config["channels"])
        self.block_check = block_check
        self.weather_apikey = weather_apikey
        self.session = aiohttp.ClientSession()
        self._all_mentions = discord.AllowedMentions.all()

        self.loop.create_task(self.on_complete())

    def reset_weather(self, apikey: str | None = None) -> None:
        self.weather_apikey = apikey or self.weather_apikey
        if not self.weather_apikey:
            raise TypeError("WEATHER_KEY is not set")
        self.weather = RatWeather(session=self.session, appid=self.weather_apikey)
        print(self.weather.data.json())
        print("Loaded weather class!")

    async def on_complete(self) -> None:
        await self.wait_until_ready()
        self.app = await self.application_info()
        print(f"Retrieved application info! (owner: {self.app.owner})")


class RatCog(commands.Cog):
    """Generic cog that all RatBot cogs can inherit from."""

    _on_ready: Callable[[], Coroutine] | None = None

    def __init__(self, bot: RatBot):
        self.bot = bot
        if self._on_ready:
            self.bot.loop.create_task(self.__on_ready__())

    async def __on_ready__(self):
        if not self._on_ready:  # satisfying the typechecker
            raise KeyError
        await self.bot.wait_until_ready()
        await self._on_ready()
