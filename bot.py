# legible ?
# good luck
# here's all the necessary imports
from datetime import datetime
from secrets import token
from time import sleep

import discord
import discord.ext.commands as commands

import config

bot = commands.Bot(command_prefix=["r.", "rat! "],
                   allowed_mentions=discord.AllowedMentions.none(),
                   intents=discord.Intents.all())

# Cog ?
if __name__ == "__main__":
    for extension in config.enabledcogs:
        try:
            bot.load_extension(extension)
        except commands.ExtensionError as e:
            print(f"{e.__class__.__name__}: {e}")


@bot.event
async def on_message(message):
    if message.author.id == 159985870458322944 and message.guild.id == 526207286067068928:
        if "you just advanced" in message.content:
            sleep(10)
            await message.delete()
    if message.author.bot: return

    # respond when anyone says my name
    if message.content.lower() == config.adminname and message.author.id != config.ratmin_id:
        await message.channel.send(config.spokesperson)
        return
    elif "ernie reads star trek fanfics" in message.content.lower():
        await message.delete()
    elif "ernie does not read star trek fanfics" in message.content.lower():
        await message.channel.send('True')
    if not message.guild or message.channel.name != "rat":
        await bot.process_commands(message)


bot.run(token)
# clouds
