import discord.ext.commands as commands
import discord
import asyncio

import secrets
import config

bot = commands.Bot(command_prefix="r,")


for Cogule in config.cogules:
      try:
            bot.load_extension(Cogule)
      except commands.ExtensionError as err:
            print(f"{err.__class__.__name__}: {err}")


@bot.event
async def on_ready():
      channel = bot.get_channel(708882977202896957)
      await channel.send("Ya Estoy En Línea Pendejos")


bot.run(secrets.token)