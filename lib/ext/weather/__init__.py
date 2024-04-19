from pathlib import Path

from .bible import getch_bible
from .message_config import MessageConfig
from .units import Units
from .weather_user import WeatherUser
from .zone_info import ZoneInfo

__all__ = [
    "getch_bible",
    "MessageConfig",
    "Units",
    "WeatherUser",
    "ZoneInfo",
    "get_message_template",
]


def get_message_template() -> str:
    cwd = Path(__file__).parent
    return (cwd / "message_template.txt").read_text()
