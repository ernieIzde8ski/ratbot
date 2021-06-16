from asyncio import get_event_loop
from discord import AllowedMentions, Intents
from discord.ext import commands

from json import load

from dotenv import load_dotenv
from os import getenv

load_dotenv()
DISCORD_TOKEN = getenv("DISCORD_TOKEN")

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
    if message.author.bot:
        return

    if "rat" in message.content.split():
        await message.channel.send("rat")

    await client.process_commands(message)


@client.command()
async def ping(ctx):
    await ctx.send("Cringe")


async def start():
    try:
        await client.start(DISCORD_TOKEN)
    except KeyboardInterrupt:
        await client.close()


async def stop():
    await client.close()


if __name__ == "__main__":
    try:
        get_event_loop().run_until_complete(start())
    except KeyboardInterrupt:
        get_event_loop().run_until_complete(stop())