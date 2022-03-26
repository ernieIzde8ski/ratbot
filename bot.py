import sys
from json import load
from os import getenv

from discord import AllowedMentions, Intents
from dotenv import load_dotenv

from utils import Blocking, RatBot, RatConfig

load_dotenv()
token = getenv("DISCORD_TOKEN")
apikey = getenv("CURRENT_WEATHER_TOKEN")

with open("config.json", "r", encoding="utf-8") as file:
    config: RatConfig = load(file)


bot = RatBot(
    allowed_mentions=AllowedMentions.none(),
    intents=Intents.all(),
    config=config,
    block_check=Blocking(),
    weather_apikey=apikey,
)

bot.load_enabled_extensions()


@bot.event
async def on_message(message):
    commands_allowed = await bot.blocking.reply(message)
    if commands_allowed:
        await bot.process_commands(message)


@bot.event
async def on_prefix_update(id, new_prefix):
    await bot.prefixes.update(id, new_prefix)


if "-DIE" in sys.argv:
    exit()

bot.run(token)
