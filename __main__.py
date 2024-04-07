#!/usr/bin/env python3
import asyncio

from lib import Bot, Settings, dirs, load_environment, load_extensions, setup_logging


async def main() -> None:
    config_dir = dirs.config_home()

    token = load_environment(config_dir)
    setup_logging(config_dir)

    settings = Settings.load_from_env()
    bot = Bot(settings)

    load_extensions(bot, settings)

    try:
        await bot.start(token)
    except (KeyboardInterrupt, asyncio.CancelledError):
        # This disables some useless noise when SIGINT'ing
        pass
    finally:
        await bot.close()


if __name__ == "__main__":
    asyncio.run(main())
