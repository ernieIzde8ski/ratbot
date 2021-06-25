class Check():
    def __init__(self):
        self.blocked = []
    
    def set_blocked(self, blocked):
        self.blocked = blocked
    
    def update_blocked(self, blockee):
        self.blocked.append(blockee.id)

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
