# bot.py
# ^ dunno what it means but i assume it serves a purpose
# here's all the necessary imports and a definition
import os
import sys
import discord
import asyncio
from datetime import datetime
import random
import config
client = discord.Client()

# this seems necessary for some dumb reason
item = 'item'
lst = 'lst'


# really shortens down some useless lines
def is_in(item, lst):
    return any(word in item for word in lst)

# defining functions for shutdown and restart
async def die():
    channel = client.get_channel(config.statusChannel)
    await channel.send('<:offline:708886391672537139> shutting down...')
    print('shutting down')
    sys.exit()
async def restart():
    channel = client.get_channel(config.statusChannel)
    await channel.send('<:restarting:708887315853869087> restarting...')
    print('restarting...')
    python = sys.executable
    os.execl(python, python, * sys.argv)


# finally, some god damnned events
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel = client.get_channel(config.statusChannel)
    await channel.send('<:online:708885917133176932> online!')


@client.event
async def on_message(message):

    auth = message.author
    if auth == client.user or message.author.bot:  # obvious return is obvious
        return

    now = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
    authID = message.author.id
    msg = message.content
    msgID = message.id
    guild = message.guild
    chan = message.channel
    coolMsgIDs = str(guild.id) + '.' + str(chan.id) + '.' + str(msgID)
    slursExist = is_in(item=msg, lst=config.slursList)

    # make rat shut down
    if msg == 'die, rat':
        await chan.send('alright chief, bring me back soon')
        await die()
        return
    # make rat restart
    elif msg == 'ratstart' and authID == config.ratminID:
        await chan.send('alright chief, hope i survive')
        await restart()
        return

    # respond when myer says my name
    elif authID == 368780147563823114 and msg.lower() == 'ernie':
        await chan.send(spokesperson)
        return

    elif 'retard' in msg:  # correct ratards
        await chan.send('*ratard')
        return

    # detect slurs & make them only work in whichever servers have opted in
    elif slursExist and is_in(item=guild.id, lst=config.guildOptIn):
        print('loser detected')
        await chan.send('loser ' + message.author.mention)
        return

    # ratmin commands (non-functioning)
    elif msg.startswith('ratmin ') or msg == 'ratmin' or msg == 'ratmint':
        print(f'[{now}] ratmin in #{chan.name} of {str(guild)} ({coolMsgIDs})')
        if authID == config.ratminID:
            if msg == 'ratmin sendhere':  # don't bother getting this to work
                await chan.send(notFunctional)
            else:
                await chan.send('bruh that\'s not a command')
                return
        else:  # if someone isn't ratmin, tell them to shut up
            await chan.send(random.choice(config.shutUp))
            return

    # the ultimate purpose: respond to rat with rat
    elif msg.startswith('rat'):
        print(f'[{now}] rat in #{chan.name} of {str(guild)} ({coolMsgIDs})')
        await chan.send('rat')
        return

#    # this is for debugging
#    elif authID == config.ratminID:
#        print('end reached')

    # any other message should reach here
    else:
        return

client.run(config.TOKEN)
# clouds
