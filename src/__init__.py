import logging
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from .bot import Bot
from .settings import Settings


def load_environment():
    file = Settings.get_config_dir() / ".env"
    if file.exists():
        load_dotenv(file, override=True)

    literal_log_level = getenv("RATBOT_LOG_LEVEL") or "INFO"
    log_level = logging._nameToLevel.get(literal_log_level.strip().upper())
    logging.basicConfig(level=log_level)
    logging.getLogger("disnake").setLevel(logging.WARNING)


def run() -> None:
    load_environment()

    token = getenv("RATBOT_TOKEN_DISCORD")
    if token is None:
        raise RuntimeError("RATBOT_TOKEN_DISCORD not set!")

    settings = Settings.load_from_env()
    bot = Bot(settings)

    bot.run(token=token)
