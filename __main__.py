from os import getenv
import discord

TOKEN = getenv("RATBOT_DISCORD_TOKEN")
assert TOKEN
client = discord.Client(intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f"'{client.user}' is online!")


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if (
        isinstance(message.channel, discord.TextChannel)
        and message.channel.name == "rat"
        and message.content != "rat"
    ):
        await message.delete()
    elif "rat" in message.content.lower().split():
        print("found a victim:")
        if message.guild:
            print(" ", message.guild.id, "|", message.guild)
            print(" ", message.channel.id, "|", message.channel)
        print(" ", message.author.id, "|", message.author)
        await message.channel.send("rat")


client.run(TOKEN)
