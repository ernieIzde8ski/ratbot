import logging
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from .bot import *
from .settings import *


def load_environment() -> str:
    config_dir = Settings.get_config_dir()

    dotenv_fp = config_dir / ".env"
    if dotenv_fp.exists():
        load_dotenv(dotenv_fp, override=True)

    token = getenv("RATBOT_TOKEN_DISCORD")
    if token is None:
        raise RuntimeError("RATBOT_TOKEN_DISCORD not set!")

    literal_log_level = getenv("RATBOT_LOG_LEVEL") or "INFO"
    log_level = logging._nameToLevel.get(literal_log_level.strip().upper())
    logging.basicConfig(level=log_level)
    logging.getLogger("disnake").setLevel(logging.WARNING)

    if (log_fp := getenv("RATBOT_LOG_FILE")) is not None:
        log_fp = log_fp.strip()
        if log_fp == "":
            path = config_dir / "log.txt"
        elif "/" not in log_fp:
            path = config_dir / log_fp
        else:
            path = Path(log_fp)

        file_handler = logging.FileHandler(path)
        file_handler.setLevel(logging.DEBUG)
        logging.getLogger().addHandler(file_handler)

    return token


def load_extensions(bot: Bot, settings: Settings) -> None:
    failed = 0
    total = len(settings.enabled_extensions)

    for ext in settings.enabled_extensions:
        try:
            bot.load_extension(ext)
        except Exception as _:
            logging.exception(f"Failed to load extension '{ext}'")
            failed += 1
        else:
            logging.debug(f"Loaded extension '{ext}'")

    if failed == 0:
        return logging.info("All extensions loaded successfully")

    ratio = failed * 10_000 // total / 100
    message = f"{ratio}% of extensions failed to load ({failed})"

    if ratio < 50:
        logging.error(message)
    else:
        logging.critical(message)
        exit()
