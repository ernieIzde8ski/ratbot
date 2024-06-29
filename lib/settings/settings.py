import logging
from pathlib import Path
from typing import Iterable, Self

from pydantic import BaseModel, Field
from yaml import safe_load

from .. import dirs
from .devel import Devel
from .raw_log_channels import RawLogChannels
from .reaction_emojis import ReactionEmojis

BASE_DIR = Path(__file__).parent.parent.parent
"""Directory containing __main__.py."""


def find_cogs_in(dir: Path, *, root: Path = BASE_DIR) -> Iterable[str]:
    """Find cogs in some directory, formatted in a way disnake understands,
    relative to a base directory."""

    for path in dir.iterdir():

        if path.name == "__pycache__":
            continue

        is_dir = path.is_dir()
        is_module = is_dir and (path / "__init__.py").exists()
        is_source_file = path.is_file() and path.suffix.lower() == ".py"

        if is_source_file:
            yield ".".join(path.relative_to(root).parts).removesuffix(".py")
        elif is_module:
            yield ".".join(path.relative_to(root).parts)
        elif is_dir:
            yield from find_cogs_in(path, root=root)
        else:
            logging.warn(f"nebulous file in cogs directory: {path.relative_to(root)}")


def find_cogs() -> list[str]:
    """Find the default cogs."""
    return list(find_cogs_in(BASE_DIR / "cogs", root=BASE_DIR))


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
