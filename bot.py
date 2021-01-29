# i dont understand half of whats here myself
# good luck
# here's all the necessary imports
from datetime import datetime
from secrets import token
from time import sleep

import discord
import discord.ext.commands as commands

import config

bot = commands.Bot(command_prefix=["r.", "rat! "], allowed_mentions=discord.AllowedMentions.none())
intents = discord.Intents.all()

# Cog ?
if __name__ == "__main__":
    for extension in config.enabledcogs:
        try:
            bot.load_extension(extension)
        except commands.ExtensionError as e:
            print(f"{e.__class__.__name__}: {e}")


def now(): return str(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))


def _removeNonAscii(s): return "".join(i for i in s if ord(i) < 384)


def msg_log(msg, msg_type):
    # if in DMs
    if msg.guild == None:
        embed = discord.Embed(title=f"DM Message from <@{msg.author.id}> ({msg.author})",
                              description=msg.content, timestamp=msg.created_at)
        return embed
    # if not
    if msg.guild.id is not None:
        embed = discord.Embed(title=f"{msg_type} in #{msg.channel.name} of {msg.guild.name}",
                              url=f"https://discordapp.com/channels/{msg.guild.id}/{msg.channel.id}/{msg.id}",
                              description=msg.content, timestamp=msg.created_at)
        return embed


# finally, some god damnned events
@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    channel = bot.get_channel(config.statusChannel)
    embed = discord.Embed(title="<:online:708885917133176932> online!", timestamp=datetime.today())
    await channel.send(embed=embed)


@bot.event
async def on_message(message):
    if message.author.id == 159985870458322944 and message.guild.id == 526207286067068928 and "you just advanced" in message.content:
        sleep(10)
        await message.delete()
    auth = message.author
    if message.author.bot: return
    msg = message.content
    msgID = message.id
    guild = message.guild
    channel = message.channel
    logChannel = bot.get_channel(config.logChannel)
    cleaned_content = message.content

    if message.author.id == 562644324832247818 and 'baza' in message.content:
        await message.delete()
        await message.channel.send('Abake Owned?')
    # respond when anyone says my name
    if msg.lower() == config.adminname and auth.id != config.ratmin_id:
        await channel.send(config.spokesperson)
        return
    elif "ernie reads star trek fanfics" in msg.lower():
        await message.delete()
    elif "ernie does not read star trek fanfics" in msg.lower():
        await channel.send('True')
    # the ultimate purpose: respond to rat with rat & moderate rat channels
    elif message.guild and (message.channel.name == "rat" and message.content != "rat"):
        try:
            await message.delete()
        except Forbidden:
            await logChannel.send(f'Lacking perms to delete a message in {guild}. Sad!')
    elif msg.startswith('rat'):
        await channel.send('rat')
        print(f"[{now()}] rat from {str(message.author)} in " + ("dms" if not message.guild else message.guild.name))

    if not message.guild or message.channel.name != "rat":
        await bot.process_commands(message)


bot.run(token)
# clouds
