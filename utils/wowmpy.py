"""
Wrapper for owmpy. 

Yes, this means I wrote a wrapper for the wrapper that I maintain. Cry about it
"""
from typing import Literal, NamedTuple

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

NamedCoords = NamedTuple("NamedCoords", lat=float, lon=float)


class WUser(BaseModel):
    coords: NamedCoords
    units: RawUnits = "metric"
    # TODO: Un-hardcode this
    guild_id: int = 488475203303768065


class WUsers(BaseModel):
    active: list[int]
    all: dict[int, WUser]


class RatWeatherData(BaseModel):
    path: str
    """Path to weather file"""
    active_users: set[int]
    """List of users to receive daily weather notifications."""
    configs: dict[int, WUser]
    """User location/unit preference data"""

    def save(self) -> None:
        with open(self.path, "w+", encoding="utf-8") as file:
            file.write(self.json(exclude={"path", "apikey"}))
        # TODO: replace instances of print() with log()
        print(f"Saved Weather object to {self.path}")


class RatWeather:
    data: RatWeatherData
    client: CurrentWeather

    users: WUsers

    def __init__(
        self, session: aiohttp.ClientSession | None = None, appid: str | None = None, path: str = "data/weather.json"
    ) -> None:
        data = safe_load(path, None) or dict(active_users=[], configs={})
        self.data = RatWeatherData(**data, path=path)
        self.client = CurrentWeather(client=session, appid=appid)

    def save(self) -> None:
        """Equivalent to obj.data.save"""
        self.data.save()

    @staticmethod
    def _units(__s: str) -> Units:
        __s = __s.lower()
        if __s not in UnitConversions:
            raise ValueError(f"Unit '{__s}' is invalid")
        return UnitConversions[__s]  # type: ignore

    async def fetch(self, *args, **kwargs):
        """Equivalent to obj.client.get"""
        return await self.client.get(*args, **kwargs)

    async def fetch_user(self, _usr: int) -> CurrentWeatherStatus:
        usr = self.users.all[_usr]
        units = UnitConversions[usr.units]
        return await self.client.get(coords=usr.coords, units=units)
