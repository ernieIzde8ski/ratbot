import logging
import re

import aiohttp
from disnake import AppInfo, Intents, Message
from disnake.ext.commands import Bot as BaseBot

from ..settings import Settings
from .log_channels import LogChannels


class Bot(BaseBot):
    """The main bot class."""

    session: aiohttp.ClientSession
    """An aiohttp session. For usage in cogs."""

    settings: Settings
    """Serializable bot settings."""

    supplements_loaded: bool = False
    """If supplementary things like log channels are finished loading."""

    logs: LogChannels
    app_info: AppInfo

    def __init__(self, settings: Settings) -> None:
        self.session = aiohttp.ClientSession()
        self.settings = settings

        intents = Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        intents.typing = False

        super().__init__(
            intents=intents,
            command_prefix=settings.prefix,
            test_guilds=settings.devel.test_guilds,
            reload=settings.devel.reloading,
        )

    async def close(self) -> None:
        await self.session.close()
        return await super().close()

    async def on_ready(self) -> None:
        """Handles setting up supplements & logging activity to a channel."""
        if self.supplements_loaded is False:
            self.logs = LogChannels(self)
            self.app_info = await self.application_info()
            self.supplements_loaded = True

            logging.info(f"Logged in as {self.user}!")
            await self.logs.status.send(f"im ALIVE {self.settings.emoji_online}")
        else:
            logging.info(f"Logged in as {self.user}! again!")
            await self.logs.status.send(
                f"im STILL ALIVE {self.settings.emoji_online * 3}"
            )

    async def on_message(self, message: Message) -> None:
        """Handles `rat` processing before handing logic over to command parsing."""
        if message.author.bot:
            return

        if getattr(message.channel, "name", None) == "rat":
            if message.content == "rat" and not message.attachments:
                await message.channel.send("rat")
            else:
                await message.delete()
        else:
            # custom event, is used in cogs
            self.dispatch("parseable_message", message, message.content.lower())
            if "rat" in re.split(r"\b", message.content):
                await message.channel.send("rat")
            await self.process_commands(message)
