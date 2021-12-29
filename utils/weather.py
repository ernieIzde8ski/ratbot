from enum import Enum

from aiohttp import ClientSession

valid_kwarg_types = {
    "city_id": int, "latitude": (int, float), "longitude": (int, float), "zip_code": (str, int),
    "country_code": str, "state_code": str, "city_name": str, "units": str, "language": str
}
valid_kwargs = list(valid_kwarg_types.keys())


class Units(Enum):
    STANDARD = {"dt": "UTC", "sunrise": "UTC", "sunset": "UTC", "temp": "Kelvin", "Humidity": "%",
                "pressure": "hPa", "speed": "meter/sec", "deg": "degrees (meteorological)",
                "gust": "meter/sec", "all": "%", "1h": "mm", "3h": "mm"}
    METRIC = {**STANDARD, "temp": "Celsius"}
    IMPERIAL = {**STANDARD, "temp": "Fahrenheit",
                "speed": "miles/hour", "gust": "miles/hour"}


class WeatherRetrieval:
    def __init__(self, apikey: str, session: ClientSession = None) -> None:
        self.session = session or ClientSession()
        self.apikey = apikey
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    async def get_weather(self, **kwargs) -> dict:
        """Returns a dict object with weather information

        takes the same parameters as get_weather_url
        """
        kwargs["appid"] = self.apikey
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
