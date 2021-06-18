from modules.msg_check import reply

from discord import AllowedMentions, Intents
from discord.ext import commands

from json import load

from dotenv import load_dotenv
from os import getenv

load_dotenv()
token = getenv("DISCORD_TOKEN")


with open("config.json", "r") as file:
    config = load(file)
    if isinstance(config.get("prefix"), str):
        config["prefix"] = [config.get("prefix")]

bot = commands.Bot(
    command_prefix=lambda b, m: commands.when_mentioned(
        b, m) + config.get("prefix"),
    allowed_mentions=AllowedMentions.none(),
    intents=Intents.all()
)
bot.config = config

with open("enabled_extensions.json", "r") as file:
    for extension in load(file):
        try:
            bot.load_extension(extension)
        except commands.ExtensionError or ModuleNotFoundError as error:
            print(f"{error.__class__.__name__}: {error}")
        else:
            print(f"Loaded extension {extension}")
    else:
        print("Loaded all extensions")


@bot.event
async def on_message(message):
    valid = await reply(message)
    if not valid: return

    await bot.process_commands(message)


bot.run(token)
