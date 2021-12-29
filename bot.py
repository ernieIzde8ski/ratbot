from json import load
from os import getenv

from discord import AllowedMentions, Intents
from discord.ext import commands
from dotenv import load_dotenv

from utils.classes import Blocking, RatBot, RatConfig


load_dotenv()
token = getenv("DISCORD_TOKEN")
apikey = getenv("WEATHER_TOKEN")

with open("config.json", "r", encoding="utf-8") as file:
    config: RatConfig = load(file)
    # The prefix can be a string, but code elsewhere does not account for that
    if isinstance(config["prefix"], str):
        config["prefix"] = [config["prefix"]]


bot = RatBot(
    allowed_mentions=AllowedMentions.none(),
    intents=Intents.all(),
    config=config,
    block_check=Blocking(),
)


if apikey:
    bot.load_weather(apikey)


with open("enabled_extensions.json", "r") as file:
    for extension in load(file):
        try:
            bot.load_extension(extension)
        except (commands.ExtensionError, ModuleNotFoundError) as error:
            print(f"{error.__class__.__name__}: {error}")
        else:
            print(f"Loaded extension {extension}")
    else:
        print("Loaded all extensions !")


@bot.event
async def on_message(message):
    valid = await bot.block_check.reply(message)
    if not valid:
        return

    await bot.process_commands(message)


@bot.event
async def on_prefix_update(id, new_prefix):
    await bot.pfx.update(id, new_prefix)


bot.run(token)
