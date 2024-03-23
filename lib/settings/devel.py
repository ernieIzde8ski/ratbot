from pydantic import BaseModel


class Devel(BaseModel):
    """Development stuff. This should mostly, if not all, be inactive in prod."""

    test_guilds: list[int] | None = None
    """Specific guilds in which to enable commands."""
    reloading: bool = False
    """Enables disnake's hot reload feature."""
