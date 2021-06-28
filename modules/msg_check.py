from modules._json import safe_load, safe_dump


class Check():
    def __init__(self):
        self.blocked = safe_load("data/blocked.json", [])

    def set_blocked(self, blocked) -> None:
        self.blocked = blocked

    def update_blocked(self, blockee) -> None:
        self.blocked.append(blockee.id)
        safe_dump("data/blocked.json", self.blocked)
    
    def unblock(self, blockee) -> None:
        self.blocked.remove(blockee.id)
        safe_dump("data/blocked.json", self.blocked)

    async def reply(self, message) -> bool:
        """Returns whether or not a message is good for command parsing"""
        if message.author.bot:
            return False
        elif message.guild:
            if message.channel.name == "rat" and (message.content != "rat" or message.attachments):
                await message.delete()
                return False

        if message.author.id in self.blocked:
            return False

        elif "rat" in message.content.split():
            await message.channel.send("rat")
        return True
