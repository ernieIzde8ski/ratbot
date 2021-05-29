# legible ?
# good luck
# here's all the necessary imports
import asyncio

import discord.ext.commands as commands
from discord import AllowedMentions, Intents, DMChannel

from configs.config import Config
from configs.enabled_cogs import enabled_cogs
from configs.secrets import token
from static import Static

intentions = Intents.all()


Config = Config()

bot = commands.Bot(command_prefix=lambda b, m: commands.when_mentioned(b, m) + Config.prefix,
                   allowed_mentions=AllowedMentions.none(),
                   intents=intentions)
bot.static = Static()
bot.config = Config

# Cog ?
for extension in enabled_cogs:
    try:
        bot.load_extension(extension)
    except commands.ExtensionError as e:
        print(f"{e.__class__.__name__}: {e}")
    except ModuleNotFoundError as e:
        print(f"{e.__class__.__name__}: {e}")
    else:
        print(f"loaded {extension}")


async def start():
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        await bot.logout()


async def stop():
    await bot.logout()


if __name__ == "__main__":
    try:
        asyncio.get_event_loop().run_until_complete(start())
    except KeyboardInterrupt:
        asyncio.get_event_loop().run_until_complete(stop())
