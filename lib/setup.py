import logging
from os import getenv
from pathlib import Path

from dotenv import load_dotenv

from lib.bot.bot import Bot
from lib.settings.settings import Settings

from . import dirs

config_dir = dirs.config_home()


def load_environment(config_dir: Path) -> str:
    dotenv_fp = config_dir / ".env"
    if dotenv_fp.exists():
        load_dotenv(dotenv_fp, override=True)

    token = getenv("RATBOT_TOKEN_DISCORD")
    if token is None:
        raise RuntimeError("RATBOT_TOKEN_DISCORD not set!")

    return token


def setup_logging(config_dir: Path) -> None:
    """Sets up root logging and such. Some environment variables are used."""
    logging.getLogger("disnake").setLevel(logging.WARNING)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    main_handler = logging.StreamHandler()
    literal_log_level = getenv("RATBOT_LOG_LEVEL") or "INFO"
    log_level = logging._nameToLevel.get(literal_log_level.strip().upper())
    if log_level is not None:
        main_handler.setLevel(log_level)
    root_logger.addHandler(main_handler)

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
        root_logger.addHandler(file_handler)


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
