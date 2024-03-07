import logging
from typing import TYPE_CHECKING, Union

from disnake import StageChannel, TextChannel, Thread

if TYPE_CHECKING:
    from ..bot import Bot

LogChannel = Union[TextChannel, Thread, StageChannel]


class LogChannels:
    status: LogChannel
    messages: LogChannel

    def __init__(self, bot: "Bot"):
        annotations = type(self).__dict__["__annotations__"]
        keys: list[str] = [s for s in annotations if annotations[s] == LogChannel]

        for key in keys:
            try:
                channel_id = getattr(bot.settings.raw_log_channels, key)
                channel = bot.get_channel(channel_id)
                assert isinstance(channel, LogChannel)
                setattr(self, key, channel)
            except Exception as _:
                logging.exception(f'Could not load "{key}" channel')
