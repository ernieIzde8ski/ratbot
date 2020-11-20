# i dont understand half of whats here myself
# good luck
# here's all the necessary imports
import discord
import discord.ext.commands as commands
import asyncio
from datetime import datetime
import random
import config
from typing import Union
from time import sleep

bot = commands.Bot(command_prefix=["r.", "rat! "])
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True

# this seems necessary for some dumb reason
item = ''
lst = ''

#Yes i think i figured out cogs this time
if __name__ == '__main__':
	for extension in config.enabledcogs:
		bot.load_extension(extension)


# is this what they call legacy code
def is_in(item, lst):
	return any(word in str(item) for word in lst)
def _removeNonAscii(s): return "".join(i for i in s if ord(i)<384)
def msg_log(msg, msg_type):
	#if in DMs
	if msg.guild == None:
		embed=discord.Embed(title = f"DM Message from <@{msg.author.id}> ({msg.author})",
		description=msg.content, timestamp=msg.created_at)
		return embed
	#if not
	if msg.guild.id != None:
		embed = discord.Embed(title = f"{msg_type} in #{msg.channel.name} of {msg.guild.name}",
		url = f"https://discordapp.com/channels/{msg.guild.id}/{msg.channel.id}/{msg.id}",
		description=msg.content, timestamp=msg.created_at)
		return embed
#[27/05/2020 16:31:23] rat in #🔬testing of Fire Nation (682704934621282307.709816228587503728.715301148004712520)
#https://discordapp.com/channels/516604644793778177/516604645418991627/715314741064499311

# finally, some god damnned events
@bot.event
async def on_ready():
	print(f'{bot.user} has connected to Discord!')
	channel = bot.get_channel(config.statusChannel)
	await channel.send('<:online:708885917133176932> online!'
	+ f'                  ({str(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))})')

@bot.event
async def on_message(message):

	if message.author.id == 159985870458322944 and message.channel.id == 759131420823650364 and "you just advanced" in message.content:
		sleep(5)
		await message.delete()
	auth = message.author
	if auth == bot.user or message.author.bot:  # obvious return is obvious
		return
	msg = message.content
	msgID = message.id
	guild = message.guild
	channel = message.channel
	slursExist = is_in(item=msg, lst=config.slursList)
	logChannel = bot.get_channel(config.logChannel)
	cleaned_content = message.content

	if guild != None:
		guild_id = guild.id
	elif guild == None:
		guild_id = None
		logChannel = bot.get_channel(config.logChannel)
		await logChannel.send(embed=msg_log(message, None))
		await bot.process_commands(message)

	if message.author.id == 562644324832247818 and 'baza' in message.content:
		await message.delete()
		await message.channel.send('Abake Owned?')
	# respond when anyone says my name
	if msg.lower() == 'ernie' and auth.id != config.ratmin_id:
		await channel.send(config.spokesperson)
		return
	elif "ernie reads star trek fanfics" in msg.lower():
		await message.delete()
	elif "ernie does not read star trek fanfics" in msg.lower():
		await channel.send('True')
	elif guild_id not in config.guildOptOut and 'retard' in msg:  # correct ratards
		await channel.send('*ratard')
		return

	# detect slurs & make them only work in whichever servers have opted in
	elif slursExist and guild_id in config.guildOptIn:
		print('loser detected')
		await channel.send('loser ' + auth.mention)
		return
	# kill tenor links lmao
	elif guild_id in config.guildOptIn and (msg.startswith('https://giphy.com/gifs/') or msg.startswith('https://tenor.com/view/')):
		await channel.send('loser ' + auth.mention)
		await message.delete()
	# the ultimate purpose: respond to rat with rat & moderate rat channels
	elif channel.name == 'rat' and msg != 'rat':
		try:
			await message.delete()
		except Forbidden:
			await logChannel.send(f'Lacking perms to delete a message in {guild}. Sad!')
	elif msg.startswith('rat'):
		await channel.send('rat')
		await logChannel.send(embed=msg_log(message, 'rat'))
	elif 'senora' in msg.lower():
		await channel.send('did you mean: Señora')
	elif 'senor' in msg.lower():
		await channel.send('did you mean: Señor')
	elif channel.name != 'rat':
		await bot.process_commands(message)


bot.run(config.TOKEN)
# clouds
