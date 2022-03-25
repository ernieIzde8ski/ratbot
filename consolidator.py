"""
Merger for old data files into a new big data file. Do NOT call more than once,
as it deletes old files but simultaneously depends on them existing.
"""

import json
from collections import defaultdict
from contextlib import suppress
from functools import partial
from pathlib import Path
from typing import Callable, TypedDict, TypeVar

from typing_extensions import NotRequired

import utils.dataclasses as dcls
from utils.wowmpy import RatWeather

DIR = Path("./data").absolute()
OBJ = {}
T = TypeVar("T")
pathlike = Path | str


def unload(path: pathlike, default: Callable[[], T]) -> T:
    """Attempts to load a file inside DIR and then deletes it, returning its contents."""
    path = DIR / path
    try:
        with open(path, "r", encoding="utf-8") as file:
            resp = json.load(file)
        path.unlink()
        return resp
    except FileNotFoundError:
        return default()


def remove(path: pathlike) -> None:
    """Unlinks a path from within DIR, if it exists."""
    with suppress(FileNotFoundError):
        (DIR / path).unlink()


def phase_1() -> dcls.SaveableModel:
    """General Data"""
    guild_ban_chances = unload("banning.json", dict)
    users_bible = unload("bible.json", dict)
    measured_alkalinities = set(unload("bm.json", list))
    emoji_wake, emoji_sleep = unload("emoji.json", partial(tuple, "🐣", "🎃"))
    emoji_laugh = unload("lmfao.json", partial(str, "🤬"))
    guilds_pipi_disabled = unload("pipi.json", list)
    songs = unload("songs.json", dict)
    emoji_trolls = unload("trolls.json", partial(list, "🧌"))
    timezones = unload("timekeeping.json", dict)
    (DIR / "russian.json").rename(DIR / "russian_bible.json")

    remove("facts.json")
    remove("trollgex.json")
    remove("tenor_guilds.json")

    emojis = dcls.RatEmojis(power_on=emoji_wake, power_off=emoji_sleep, laugh=emoji_laugh, trolls=emoji_trolls)

    guilds: defaultdict[int, dcls.RatGuildConfigs] = defaultdict(dcls.RatGuildConfigs)
    for gid, chance in guild_ban_chances.items():
        guilds[int(gid)].ban_chance = float(chance)
    for gid in guilds_pipi_disabled:
        guilds[int(gid)].pipi_enabled = False

    users: defaultdict[int, dcls.RatUserConfigs] = defaultdict(dcls.RatUserConfigs)
    for uid, ver in users_bible.items():
        users[int(uid)].preferred_version = ver
    for uid, tz in timezones.items():
        users[int(uid)].tz = tz

    return dcls.RatSettings(
        path="data/settings.json",
        songs=songs,
        emojis=emojis,
        guilds=guilds,
        users=users,
        measured=measured_alkalinities,
    )


def phase_2() -> dcls.SaveableModel:
    """Weather Data"""
    # I kinda keep forgetting how to write this shit so I typed it
    class UserLocation(TypedDict):
        units: NotRequired[str]
        lat: NotRequired[float]
        lon: NotRequired[float]

    UserDatum = TypedDict("UserDatum", tz=str, aliases=list[str], sent=str, location=UserLocation)
    UserData = TypedDict("UserData", {"active": list[int], "_": dict[str, UserDatum]})

    user_data = unload("weather_users.json", partial(UserData))  # Yes, it'll raise an error
    responses = unload("weather_resps.json", dict)

    active_users = set(user_data["active"])
    all_users = defaultdict(dcls.WUser)
    for uid, datum in user_data["_"].items():
        user = all_users[uid]
        user.tz = datum["tz"]
        user.aliases = set(datum["aliases"])
        if "units" in datum["location"]:
            user.units = RatWeather.validate_units(datum["location"]["units"]).api_name  # type: ignore
        if "lat" in datum["location"] and "lon" in datum["location"]:
            user.coords.lat = datum["location"]["lat"]

    users = dcls.WUsers(active=active_users, all=all_users)

    resps = dcls.RatWeatherResponses(
        greetings=set(responses["greetings"]),
        temp_reactions=sorted((tuple(i) for i in responses["temperature_resps"]), key=lambda i: i[0]),
    )

    return dcls.RatWeatherData(path="data/weather.json", users=users, resps=resps)


def main():
    for i, foo in enumerate((phase_1, phase_2)):
        model = foo()
        model.save()
        print(f"Phase {i+1}: '{foo.__doc__}' is complete")


if __name__ == "__main__":
    main()
