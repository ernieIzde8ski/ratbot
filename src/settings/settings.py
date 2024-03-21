import functools
import logging
import os
from pathlib import Path
from typing import Self

from pydantic import BaseModel, Field
from xdg_base_dirs import xdg_config_home
from yaml import safe_load

from .raw_log_channels import RawLogChannels


class Settings(BaseModel):

    """
    Serializable settings format.

    Default values are given for each attribute. If a file exists at
    `($RATBOT_CONFIG_DIR or $XDG_CONFIG_DIR)/config.yaml`, it overrides defaults.
    """

    default_prefix: str = "r."
    raw_log_channels: RawLogChannels = Field(default_factory=RawLogChannels)
    emoji_online: str = "<:online:708885917133176932>"

    @functools.cache
    @staticmethod
    def get_config_dir() -> Path:
        env_path: str | None = os.getenv("RATBOT_CONFIG_DIR")
        if env_path is None:
            return xdg_config_home() / "ratbot"
        else:
            return Path(env_path)

    @classmethod
    def load_from_env(cls) -> Self:
        fp = cls.get_config_dir() / "config.yaml"

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
