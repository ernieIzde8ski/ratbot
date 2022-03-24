from typing import Any, Coroutine, Literal, NamedTuple

import aiohttp
from owmpy.current import CurrentWeather, CurrentWeatherStatus, StandardUnits, Units
from pydantic import BaseModel

from utils.functions import safe_load


RawUnits = Literal["standard", "metric", "imperial"]
UnitConversions: dict[RawUnits, Units] = {
    "standard": StandardUnits.STANDARD,
    "metric": StandardUnits.METRIC,
    "imperial": StandardUnits.IMPERIAL,
}

NamedCoords = NamedTuple("Coords", lat=float, lon=float)


class _User(BaseModel):
    coords: NamedCoords
    units: RawUnits = "metric"
    # TODO: Un-hardcode this
    server: int = 488475203303768065


class _Users(BaseModel):
    active: list[int]
    all: dict[int, _User]


class RatWeatherData(BaseModel):
    path: str
    """Path to weather file"""
    active_users: list[int]
    """List of users to receive daily weather notifications."""
    configs: dict[int, _User]
    """User location/unit preference data"""

    def save(self) -> None:
        with open(self.path, "w+", encoding="utf-8") as file:
            file.write(self.json(exclude={"path", "apikey"}))
        # TODO: replace instances of print() with log()
        print(f"Saved Weather object to {self.path}")


class RatWeather:
    data: RatWeatherData
    client: CurrentWeather

    users: _Users

    def __init__(
        self, session: aiohttp.ClientSession | None = None, appid: str | None = None, path: str = "data/weather.json"
    ) -> None:
        self.data = RatWeatherData(**safe_load(path), path=path)
        self.client = CurrentWeather(client=session, appid=appid)

    def save(self) -> None:
        """Equivalent to obj.data.save"""
        self.data.save()

    async def fetch(self, *args, **kwargs):
        """Equivalent to obj.client.get"""
        print("i")
        return await self.client.get(*args, **kwargs)

    async def fetch_user(self, _usr: int) -> CurrentWeatherStatus:
        usr = self.users.all[_usr]
        units = UnitConversions[usr.units]
        return await self.client.get(coords=usr.coords, units=units)
