#!/usr/bin/env python3
import asyncio
from contextlib import suppress

from lib import Bot, Settings, load_environment, load_extensions


async def main() -> None:
    token = load_environment()

    settings = Settings.load_from_env()
    bot = Bot(settings)

    load_extensions(bot, settings)

    with suppress(KeyboardInterrupt):
        await bot.start(token)


if __name__ == "__main__":
    asyncio.run(main())
