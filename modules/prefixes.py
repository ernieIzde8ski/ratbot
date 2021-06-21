from json import load, dump
from discord.ext.commands import when_mentioned, when_mentioned_or

class Prefixes:
    def __init__(self, default_prefix):
        self.prefix = default_prefix
        try:
            with open("data/prefixes.json", "r", encoding="utf-8") as file:
                self.prefixes = load(file)
        except FileNotFoundError:
            self.prefixes = {}
            with open("data/prefixes.json", "x") as file:
                dump(self.prefixes, file)

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
        with open("data/prefixes.json", "w", encoding="utf-8") as file:
            dump(self.prefixes, file)
