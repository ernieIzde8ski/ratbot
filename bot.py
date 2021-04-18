# legible ?
# good luck
# here's all the necessary imports
import asyncio

import discord.ext.commands as commands
import hypixelaPY.exceptions as hypixele
from discord import AllowedMentions, Intents
from hypixelaPY import Hypixel

from configs.config import Config
from configs.enabled_cogs import enabled_cogs
from configs.secrets import token, hypixel_api_key
from static import Static

intentions = Intents.all()

Config = Config()
bot = commands.Bot(command_prefix=Config.prefix,
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
        try:
            bot.hypixel = await Hypixel(hypixel_api_key)
        except hypixele.InvalidAPIKeyError as error:
            print(f"hypixelaPY.exceptions.InvalidAPIKeyError: {error}")
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
