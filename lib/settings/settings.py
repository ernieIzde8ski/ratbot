import logging
from pathlib import Path
from typing import Self

from pydantic import BaseModel, Field
from yaml import safe_load

from .. import dirs
from .devel import Devel
from .raw_log_channels import RawLogChannels
from .reaction_emojis import ReactionEmojis

base_dir = Path(__file__).parent.parent.parent
"""Directory containing __main__.py."""


def find_cogs() -> list[str]:
    resp = []

    paths = (base_dir).joinpath("cogs").rglob("*.py")

    for path in paths:
        index = path.parts.index("cogs")
        parts = path.parts[index:]
        cog = ".".join(parts).removesuffix(".py")
        resp.append(cog)

    return resp


class Settings(BaseModel):
    """
    Serializable settings format.

    Default values are given for each attribute. If a file exists at
    `($RATBOT_CONFIG_DIR or $XDG_CONFIG_DIR)/config.yaml`, it overrides defaults.
    """

    devel: Devel = Field(default_factory=Devel)
    emoji_online: str = "<:online:708885917133176932>"
    emoji_offline: str = "<:offline:708886391672537139>"
    enabled_extensions: list[str] = Field(default_factory=find_cogs)
    hide_mod_commands: bool = False
    prefix: str = "r."
    """Text-based command prefix."""
    raw_log_channels: RawLogChannels = Field(default_factory=RawLogChannels)

    dm_expiry_delay: float = 300.0
    """cogs.events.direct_messages: delay in seconds before the latest_message expires"""

    reaction_emojis: list[ReactionEmojis] = Field(
        default_factory=lambda: [ReactionEmojis.default]
    )
    """for cogs.events.reactions."""

    @classmethod
    def load_from_env(cls) -> Self:
        fp = dirs.config_home() / "config.yaml"

        if not fp.exists():
            logging.warning("Configuration file does not exist. Using defaults.")
            logging.warning(
                "You can suppress this warning by creating a blank file:\n\t" + str(fp)
            )
            return cls()

        with open(fp, "r") as file:
            contents = safe_load(file.read())

        if contents is None:
            return cls()
        return cls(**contents)
