from typing import Any, Type, TypedDict
from typing_extensions import NotRequired

Bible = dict[str, str]
""" A dictionary mapping member ID to translation. Corresponds to bible.json. """

Russian = list[str]
""" A list of bible verses. Corresponds to russian.json. """


class WeatherResps(TypedDict):
    """Corresponds to weather_resps.json"""

    greetings: list[str]
    temperature_resps: list[tuple[int, str]]


class _WeatherLocation(TypedDict, total=False):
    units: str
    lang: str

    q: str
    id: str | int
    lat: str | int
    lon: str | int
    zip: str


class _WeatherUser(TypedDict):
    location: dict[str, _WeatherLocation]
    tz: NotRequired[Any]
    sent: NotRequired[str]


class WeatherUsers(TypedDict):
    """Corresponds to weather_users.json"""

    active: list[str]
    _: dict[str, _WeatherUser]
