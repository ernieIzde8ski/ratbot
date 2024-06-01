import functools
import typing
from os import getenv
from pathlib import Path

from xdg_base_dirs import xdg_config_home, xdg_data_home

__all__ = ["config_home", "data_home", "weather_home"]

PathFunc = typing.Callable[[], Path]
"""A function that takes no input and spits out a path."""


def cached_path(outer: PathFunc) -> PathFunc:
    @functools.cache
    def inner() -> Path:
        path = outer()
        if not path.exists():
            path.mkdir()
        return path

    return inner


@cached_path
def config_home() -> Path:
    env_fp = getenv("RATBOT_CONFIGS")
    if env_fp is None:
        return xdg_config_home() / "ratbot"
    else:
        return Path(env_fp)


@cached_path
def data_home() -> Path:
    env_fp = getenv("RATBOT_DATA")
    if env_fp is None:
        return xdg_data_home() / "ratbot"
    else:
        return Path(env_fp)


@cached_path
def weather_home() -> Path:
    return config_home() / "weather"
