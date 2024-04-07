from functools import cache
from os import getenv
from pathlib import Path

from xdg_base_dirs import xdg_config_home, xdg_data_home


@cache
def config_home() -> Path:
    env_fp = getenv("RATBOT_CONFIGS")
    if env_fp is None:
        return xdg_config_home() / "ratbot"
    else:
        return Path(env_fp)


@cache
def data_home() -> Path:
    env_fp = getenv("RATBOT_DATA")
    if env_fp is None:
        return xdg_data_home() / "ratbot"
    else:
        return Path(env_fp)


@cache
def weather_home() -> Path:
    return config_home() / "weather"
