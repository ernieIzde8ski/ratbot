from modules.json import safe_dump, safe_load
from json import load, dump
from discord.ext.commands import when_mentioned, when_mentioned_or

class Prefixes:
    def __init__(self, default_prefix):
        self.prefix = default_prefix
        self.prefix = safe_load("data/prefixes.json", {})

    async def get_prefix(self, bot, message):
        if not message.guild:
            return when_mentioned(bot, message) + self.prefix
        id = str(message.guild.id)
        if not self.prefixes.get(id):
            return when_mentioned(bot, message) + self.prefix
        else:
            return when_mentioned_or(self.prefixes[id])(bot, message)
    
    async def update_prefixes(self, id, new_prefix):
        self.prefixes[id] = new_prefix
        safe_dump("data/prefixes.json", self.prefixes)
