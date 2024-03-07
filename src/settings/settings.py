import functools
import logging
import os
from pathlib import Path
from typing import Self

from pydantic import BaseModel, Field
from xdg_base_dirs import xdg_config_home
from yaml import safe_load

from .log_channels import LogChannels


class Settings(BaseModel):

    """
    Serializable settings format.

    Default values are given for each attribute. If a file exists at
    `($RATBOT_CONFIG_DIR or $XDG_CONFIG_DIR)/config.yaml`, it overrides defaults.
    """

    default_prefix: str = "r."
    log_channels: LogChannels = Field(default_factory=LogChannels)

    @functools.cache
    @staticmethod
    def get_path() -> Path:
        env_path: str | None = os.getenv("RATBOT_CONFIG_DIR")
        if env_path is None:
            return xdg_config_home() / "ratbot" / "config.yaml"
        else:
            return Path(env_path) / "config.yaml"

    @classmethod
    def load_from_env(cls) -> Self:
        fp = cls.get_path()

        if not fp.exists():
            logging.warning("Configuration file does not exist. Using defaults.")
            logging.warning(
                "You can suppress this warning by creating a blank file:\n\t" + str(fp)
            )
            return cls()

        with open(fp, "r") as file:
            contents = safe_load(file.read())

        return cls(**contents)
