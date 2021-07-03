from modules._json import safe_dump, safe_load
from discord.ext.commands import when_mentioned, when_mentioned_or


class Prefixes:
    def __init__(self, default_prefix):
        self.prefix = default_prefix
        self.prefixes = safe_load("data/prefixes.json", {})

    async def get(self, bot, message) -> list:
        """Returns a prefix off of context"""
        if not message.guild:
            return when_mentioned(bot, message) + self.prefix
        id = str(message.guild.id)
        if not self.prefixes.get(id):
            return when_mentioned(bot, message) + self.prefix
        else:
            return when_mentioned_or(self.prefixes[id])(bot, message)

    async def update(self, id: str, new_prefix: str) -> None:
        """Update a guild's prefix"""
        self.prefixes[id] = new_prefix
        safe_dump("data/prefixes.json", self.prefixes)

    async def reset(self, id: str) -> None:
        """Reset a guild's prefix"""
        self.prefixes.pop(id)
