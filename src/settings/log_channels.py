from pydantic import BaseModel


class LogChannels(BaseModel):
    """Discord Channel IDs."""

    status: int = 1015705231566319717
    """Uptime status messages."""

    messages: int = 1097921070486540299
    """Direct messages to/from rat."""
