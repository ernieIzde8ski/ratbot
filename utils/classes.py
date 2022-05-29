import asyncio
import typing

import aiohttp
import discord
from discord.ext import commands

from .dataclasses import *
from .functions import safe_dump, safe_load
from .wowmpy import RatWeather


def return_none():
    pass


class StatusChannels:
    # TODO: Load this under a cog instead and make it a @dataclass
    BM: discord.TextChannel
    DM: discord.TextChannel
    Status: discord.TextChannel
    Guilds: discord.TextChannel

    def __init__(self, channels: config_channels):
        self.config_channels = channels
        self.loaded = False

    def get_channels(self, bot: "RatBot") -> None:
        """Retrieve channels for later usage"""
        for k, v in self.config_channels.items():
            c = bot.get_channel(v)
            if c is None:
                print(f"Could not get channel {k} from id {v}")
            setattr(self, k, c)
        self.loaded = True


class Blocking:
    """Handles blocking/unblocking users"""

    path = "data/blocked.json"
    blocked: set[int] = set(safe_load(path, []))
    """User IDs from blocked individuals"""

    def __iter__(self):
        yield from self.blocked

    def save(self):
        safe_dump(self.path, self.blocked)

    def add(self, blockee: discord.User | discord.Member) -> None:
        self.blocked.add(blockee.id)  # type: ignore
        self.save()

    def remove(self, blockee: discord.User | discord.Member) -> None:
        self.blocked.remove(blockee.id)  # type: ignore
        self.save()

    async def reply(self, message: discord.Message) -> bool:
        """Returns whether or not a message is good for command parsing"""
        if message.author.bot or message.author.id in self:  # type: ignore
            return False
        elif isinstance(message.channel, discord.TextChannel):
            if message.channel.name == "rat" and (message.content != "rat" or message.attachments):
                await message.delete()
                return False

        if "rat" in message.content.split():
            await message.channel.send("rat")

        return True


class Prefixes:
    """Command prefix handling"""

    path: str = "data/prefixes.json"
    default: list[str]
    """The default prefix(es)."""
    prefixes: dict[int, str]
    """Guild-specific prefixes"""

    def __init__(self, default: list[str]):
        prefixes = safe_load(self.path, {})
        self.default = default
        self.prefixes = {int(k): v for k, v in prefixes.items()}

    def save(self):
        safe_dump(self.path, self.prefixes)

    async def get(self, bot: "RatBot", message: discord.Message) -> list:
        """Return a prefix based off of context"""
        if message.guild is None:
            return commands.when_mentioned_or("", *self.default)(bot, message)
        prefix = self.prefixes.get(message.guild.id)  # type: ignore
        if prefix is None:
            return commands.when_mentioned_or(*self.default)(bot, message)
        else:
            return commands.when_mentioned_or(prefix)(bot, message)

    async def update(self, __id: int, new_prefix: str) -> None:
        """Update a guild's prefix"""
        self.prefixes[__id] = new_prefix
        safe_dump("data/prefixes.json", self.prefixes)

    async def reset(self, __id: int) -> str:
        """Reset a guild's prefix, returning it"""
        return self.prefixes.pop(__id)


class RatBot(commands.Bot):
    weather: RatWeather
    weather_apikey: str | None

    def __init__(self, *args, weather_apikey: str | None = None, **kwargs):
        self.config = RatConfig.load(path="config.json", default_kwargs={})
        self.prefixes = Prefixes(self.config.prefix)
        super().__init__(*args, command_prefix=self.prefixes.get, **kwargs)

        self.settings = RatSettings.load("data/settings.json", default_kwargs={})
        self.status_channels = StatusChannels(self.config.channels)
        self.blocking = Blocking()
        self.weather_apikey = weather_apikey
        self.session = aiohttp.ClientSession()

        self._all_mentions = discord.AllowedMentions.all()

    async def load_enabled_extension(self, ext: str, /):
        try:
            await self.load_extension(ext)
        except (commands.ExtensionError, ModuleNotFoundError) as err:
            print(f"{err.__class__.__name__}: {err}")
        else:
            print(f"Loaded extension {ext}!")

    async def load_enabled_extensions(self):
        # TODO: maybe disabled extensions instead of enabled
        loader = (self.load_enabled_extension(ext) for ext in self.config.enabled_extensions)
        await asyncio.gather(*loader)
        print("Loaded all extensions?!")

    async def setup_hook(self) -> None:
        await self.load_enabled_extensions()
        self.app = await self.application_info()
        print(f"Retrieved application info! (owner: {self.app.owner})")

    def reset_weather(self, apikey: str | None = None) -> None:
        self.weather_apikey = apikey or self.weather_apikey
        if not self.weather_apikey:
            raise TypeError("WEATHER_KEY is not set")
        self.weather = RatWeather(session=self.session, appid=self.weather_apikey)
        print("Loaded weather class!")


class RatCog(commands.Cog):
    """Generic cog that all RatBot cogs can inherit from."""

    _on_ready: typing.Callable[[], typing.Coroutine] | None = None

    def __init__(self, bot: RatBot):
        # Convenient aliases
        self.bot = bot
        self.config = self.bot.config
        self.guilds = self.bot.settings.guilds
        self.users = self.bot.settings.users
        self.songs = self.bot.settings.songs
        self.emojis = self.bot.settings.emojis

        if self._on_ready:
            self.bot.loop.create_task(self.__on_ready__())

    async def __on_ready__(self):
        if not self._on_ready:  # satisfying the typechecker
            raise KeyError
        await self.bot.wait_until_ready()
        coroutine = self._on_ready()
        if not isinstance(coroutine, typing.Coroutine):
            raise TypeError(f"Method _on_ready in class '{type(self).__name__}' does not return a coroutine!")
        await coroutine

    @classmethod
    async def basic_setup(cls, bot: RatBot):
        await bot.add_cog(cls(bot))
