from modules.run import run
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

client = commands.Bot(
    command_prefix=lambda b, m: commands.when_mentioned(b, m) + config.get("prefix"),
    allowed_mentions=AllowedMentions.none(),
    intents=Intents.all()
)
client.config = config


@client.event
async def on_message(message):
    valid = await reply(message)
    if not valid: return

    await client.process_commands(message)


@client.command()
async def ping(ctx):
    await ctx.send("Cringe")


run(client, token)
