"""
Wrapper for owmpy. 

Yes, this means I wrote a wrapper for the wrapper that I maintain. Cry about it
"""

import aiohttp
from owmpy.current import (CurrentWeather, CurrentWeatherStatus, StandardUnits,Units)

from .dataclasses import (RatWeatherData, RatWeatherResponses, RawUnits, WUser, WUserCoords, WUsers)
from .functions import safe_load

UnitConversions: dict[RawUnits, Units] = {
    "standard": StandardUnits.STANDARD,
    "metric": StandardUnits.METRIC,
    "imperial": StandardUnits.IMPERIAL,
}


class RatWeather:
    data: RatWeatherData
    client: CurrentWeather

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
    def validate_units(__s: str) -> Units:
        __s = __s.lower()
        if __s not in UnitConversions:
            raise ValueError(f"Unit '{__s}' is invalid")
        return UnitConversions[__s]  # type: ignore

    async def fetch(self, *args, **kwargs):
        """Equivalent to obj.client.get"""
        return await self.client.get(*args, **kwargs)

    async def fetch_user(self, __id: int) -> CurrentWeatherStatus:
        user = self.data.users.all[__id]
        return await self.client.get(coords=tuple(user.coords), units=self.validate_units(user.units))
