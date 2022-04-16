import sys
from os import getenv

from discord import AllowedMentions, Intents
from dotenv import load_dotenv

from utils import Blocking, RatBot

load_dotenv()
token = getenv("DISCORD_TOKEN")
apikey = getenv("CURRENT_WEATHER_TOKEN")


bot = RatBot(
    allowed_mentions=AllowedMentions.none(), intents=Intents.all(), block_check=Blocking(), weather_apikey=apikey
)


@bot.event
async def on_message(message):
    commands_allowed = await bot.blocking.reply(message)
    if commands_allowed:
        await bot.process_commands(message)


@bot.event
async def on_prefix_update(id, new_prefix):
    await bot.prefixes.update(id, new_prefix)


if __name__ == "__main__":
    if "--die" in sys.argv or "-D" in sys.argv:
        exit()
    bot.run(token)
