from disnake import Intents, Message, TextChannel
from disnake.ext.commands import Bot as BaseBot

from ..settings import Settings
from .log_channels import LogChannels


class Bot(BaseBot):
    """The main bot class."""

    settings: Settings
    """Serializable bot settings."""

    supplements_loaded: bool = False
    """If supplementary things like log channels are finished loading."""

    logc: LogChannels

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

        intents = Intents.default()
        intents.message_content = True
        super().__init__(intents=intents, command_prefix=settings.default_prefix)

    async def on_ready(self) -> None:
        """Handles setting up supplements & logging activity to a channel."""
        if self.supplements_loaded is False:
            self.logc = LogChannels(self)
            self.supplements_loaded = True

    async def on_message(self, message: Message) -> None:
        """Handles `rat` processing before handing logic over to command parsing."""
        if message.author.bot:
            return

        if isinstance(message.channel, TextChannel) and message.channel.name == "rat":
            if message.content == "rat" and not message.attachments:
                await message.channel.send("rat")
            else:
                await message.delete()
        else:
            if "rat" in message.content:
                await message.channel.send("rat")
            await self.process_commands(message)
