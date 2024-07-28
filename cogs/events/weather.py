import json
import logging
import traceback
from typing import TYPE_CHECKING

from discord.ext import commands
import discord
from fuzzywuzzy import fuzz
from owmpy.current import CurrentWeather
from owmpy.utils import convert_temp, Units, StandardUnits
from settings import channels, settings, root, Saveable
from utils import RatCog, RatCtx, codeblock
from os import getenv
from dotenv import load_dotenv
from pydantic import BaseModel, parse_file_as, parse_obj_as


############


def get_units_by_name(name: str, /):
    res = {
        "imperial": StandardUnits.IMPERIAL,
        "metric": StandardUnits.METRIC,
        "standard": StandardUnits.STANDARD,
    }.get(name.lower())
    if res is None:
        raise ValueError(f"invalid unit name: '{name}'")
    return res


class WeatherRecipient(BaseModel):
    coords: tuple[int, int]
    """Latitude/longitude weather location."""
    preferred_units: Units
    """Metric, imperial, or standard."""
    active: bool = True
    last_sent: str = "<UNSENT>"


class WeatherRecipientsModel(Saveable):
    __root__: dict[int, WeatherRecipient]
    _path = root / "settings.weather.json"

    def __getitem__(self, __key: int):
        return self.__root__.__getitem__(__key)

    def __setitem__(self, __key: int, __value: WeatherRecipient):
        return self.__root__.__setitem__(__key, __value)


############


class WeatherNotifications(RatCog):
    async def cog_load(self):
        # preferable to reload dotenv without restarting bot while devving
        if settings.debug:
            load_dotenv()

        key = getenv("CURRENT_WEATHER_TOKEN")
        if not key:
            raise RuntimeError("CURRENT_WEATHER_TOKEN env variable is not set")

        self.recipients = WeatherRecipientsModel.load()
        if self.recipients.__root__ == {}:
            self.recipients.save()

        # load last to avoid issues when session is unclosed
        self.client = CurrentWeather(key)

    async def cog_unload(self) -> None:
        await self.client.close()

    @commands.hybrid_group()
    async def weather(self, ctx: RatCtx):
        await ctx.send("I am the Spooky Weather Ghost")
    
    @weather.command()
    async def add(self, ctx: RatCtx, user: discord.User | None):
        """Add your weather information to ratbot."""

    @commands.Cog.listener()
    async def on_member_update(self, old: discord.Member, new: discord.Member):
        pass


setup = WeatherNotifications.basic_setup
