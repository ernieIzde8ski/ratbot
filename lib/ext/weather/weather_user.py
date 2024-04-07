from datetime import date, timedelta

from owmpy.utils.standard_units import StandardUnits
from pydantic import BaseModel

from .units import Units
from .zone_info import ZoneInfo


class WeatherUser(BaseModel):
    """Someone to send weather updates to."""

    aliases: list[str]
    """Names to call this user in the message."""
    enabled: bool = True
    """Whether to send this user messages or not."""

    coords: tuple[float, float]
    """Latitude, longitude."""
    preferred_units: Units = StandardUnits.METRIC
    """One of metric, imperial, or 'standard' (scientific)."""

    watched_guild: int
    """ID of Discord Guild to monitor status changes from."""
    last_sent: date | None = None
    """Last day that a message was sent."""
    offset: timedelta = timedelta(hours=4)
    """How long to wait after midnight before sending a new message."""
    timezone: ZoneInfo
    """Self-explanatory."""
