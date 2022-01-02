from typing import TypedDict
from typing_extensions import NotRequired


Clouds = TypedDict("Clouds", {"all": int})

Coords = TypedDict("Coords", {"lon": float | int, "lat": float | int})


class Main(TypedDict):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int
    sea_level: NotRequired[int]
    grnd_level: NotRequired[int]


class Sys(TypedDict):
    type: NotRequired[int]
    id: NotRequired[int]
    country: NotRequired[str]
    sunrise: int
    sunset: int


_WRU = TypedDict("_WRU", {"1h": str, "3h": str})


class Units(_WRU):
    dt: str
    sunrise: str
    sunset: str
    temp: str
    Humidity: str
    pressure: str
    speed: str
    deg: str
    gust: str
    all: str


class WeatherResponseWeather(TypedDict):
    id: int
    main: str
    description: str
    icon: str


class Wind(TypedDict):
    speed: float
    deg: int
    gust: NotRequired[float]


class WeatherResponseType(TypedDict):
    base: str
    clouds: Clouds
    cod: int
    coord: Coords
    dt: int
    id: int
    main: Main
    name: str
    snow: NotRequired[dict]
    sys: Sys
    timezone: int
    units: Units
    visibility: int
    weather: list[WeatherResponseWeather]
    wind: Wind


WeatherResponseError = TypedDict("WeatherError", {"error": str})


class FixedKwargs(TypedDict, total=False):
    appid: str

    units: str
    lang: str

    q: str
    id: str | int
    lat: str | int
    lon: str | int
    zip: str
