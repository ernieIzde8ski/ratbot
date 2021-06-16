async def reply(message) -> bool:
    """Returns whether or not a message is good for command parsing"""
    if message.author.bot:
        return False
    elif message.channel.name == "rat":
        if message.content != "rat" or message.attachments:
            await message.delete()
            return False

    if "rat" in message.content.split():
        await message.channel.send("rat")
    return True
