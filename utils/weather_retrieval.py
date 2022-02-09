from enum import Enum

from aiohttp import ClientSession

from utils.weather_retrieval_types import FixedKwargs, WeatherResponseError, WeatherResponseType

valid_kwarg_types = {
    "city_id": int,
    "lat": (int, float),
    "lon": (int, float),
    "zip_code": (str, int),
    "country_code": str,
    "state_code": str,
    "city_name": str,
    "units": str,
    "lang": str,
}
valid_kwargs = list(valid_kwarg_types.keys())


_STANDARD = {
    "dt": "UTC",
    "sunrise": "UTC",
    "sunset": "UTC",
    "temp": "Kelvin",
    "Humidity": "%",
    "pressure": "hPa",
    "speed": "meter/sec",
    "deg": "degrees (meteorological)",
    "gust": "meter/sec",
    "all": "%",
    "1h": "mm",
    "3h": "mm",
}
_METRIC = {**_STANDARD, "temp": "Celsius"}
_IMPERIAL = {**_STANDARD, "temp": "Fahrenheit", "speed": "miles/hour", "gust": "miles/hour"}


class Units(Enum):
    """Enum of units. Deprecated? Maybe"""

    STANDARD = _STANDARD
    METRIC = _METRIC
    IMPERIAL = _IMPERIAL


class WeatherRetrieval:
    def __init__(self, apikey: str, session: ClientSession = None) -> None:
        self.session = session or ClientSession()
        self.apikey = apikey
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    def fix_kwargs(
        apikey: str,
        *,
        q: str = None,
        city_name: str = None,
        state_code: str = None,
        country_code: str = None,
        city_id: int | str = None,
        lat: int | str = None,
        lon: int | str = None,
        latitude: int | str = None,
        longitude: int | str = None,
        zip_code: int | str = None,
        units: str = "metric",
        lang: str = None,
    ) -> FixedKwargs:
        resp = FixedKwargs(appid=apikey)

        if q:
            resp["q"] = q
        elif city_name:
            query: list[str] = []
            for i in (city_name, state_code, country_code):
                if i:
                    query.append(i)
                else:
                    break
            resp["q"] = ",".join(query)
        elif city_id:
            resp["id"] = city_id
        elif lat is not None and lon is not None:
            resp["lat"] = lat
            resp["lon"] = lon
        elif latitude is not None and longitude is not None:
            resp["lat"] = latitude
            resp["lon"] = longitude
        elif zip_code:
            resp["zip"] = ",".join(str(i) for i in (zip_code, country_code) if i)

        resp["units"] = units
        if lang:
            resp["lang"] = lang

        return resp

    async def get_weather(self, **kwargs) -> WeatherResponseType | WeatherResponseError:
        """Returns a dict object with weather information

        takes the same parameters as get_weather_url
        """
        kwargs = self.fix_kwargs(self.apikey, **kwargs)
        async with self.session.get(self.base_url, **{"params": kwargs}) as resp:
            resp = await resp.json()
            if resp.get("message"):
                return {"error": resp["message"]}
            if (units := kwargs.get("units")) is not None:
                units = units.title()
                if units == "Imperial":
                    resp["units"] = Units.IMPERIAL.value
                elif units == "Metric":
                    resp["units"] = Units.METRIC.value
                else:
                    resp["units"] = Units.STANDARD.value
            else:
                resp["units"] = Units.METRIC.value
            return resp
