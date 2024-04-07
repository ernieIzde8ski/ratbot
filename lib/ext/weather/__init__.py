from .bible import getch_bible
from .message_config import MessageConfig
from .units import Units
from .weather_user import WeatherUser
from .zone_info import ZoneInfo


def get_message_template() -> str:
    from pathlib import Path

    cwd = Path(__file__).parent
    return (cwd / "message_template.txt").read_text()
