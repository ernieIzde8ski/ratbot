# legible ?
# good luck
# here's all the necessary imports
from secrets import token, api_key

from hypixelaPY import Hypixel
import asyncio
import discord
import discord.ext.commands as commands

from static import Static
from config import Config

intentions = discord.Intents.all()
intentions.presences = False  # why ? - myer

bot = commands.Bot(command_prefix=["r.", "rat! "],
                   allowed_mentions=discord.AllowedMentions.none(),
                   intents=intentions)
bot.static = Static()
bot.config = Config()

# Cog ?
for extension in bot.config.enabledcogs:
    try:
        bot.load_extension(extension)
    except commands.ExtensionError as e:
        print(f"{e.__class__.__name__}: {e}")


async def start():
    try:
        bot.hypixel = await Hypixel(api_key)
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
