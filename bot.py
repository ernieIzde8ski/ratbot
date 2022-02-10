import json
from json import load
from os import getenv
from typing import Iterable

from discord import AllowedMentions, Intents
from discord.ext import commands
from dotenv import load_dotenv

from utils.classes import Blocking, RatBot, RatConfig

load_dotenv()
token = getenv("DISCORD_TOKEN")

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

# TODO: Disabled extensions, instead of enabled extensions
ENABLED_EXTS_PATH = "enabled_extensions.json"
with open(ENABLED_EXTS_PATH, "r") as f1:
    exts: set[str] = load(f1)
    if len(exts) != len(exts := set(exts)):
        with open(ENABLED_EXTS_PATH, "w") as f2:
            json.dump(sorted(exts), f2)
    for ext in exts:
        try:
            bot.load_extension(ext)
        except (commands.ExtensionError, ModuleNotFoundError) as error:
            print(f"{error.__class__.__name__}: {error}")
        else:
            print(f"Loaded extension {ext}")
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
