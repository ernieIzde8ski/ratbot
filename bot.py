# bot.py 
# ^ dunno what it means but i assume it serves a purpose
import os
import sys
import discord
import asyncio
from datetime import datetime
import random
import config

client = discord.Client()

def is_in(symbol, lst):
    return any(symbol in x for x in lst)

def restart():
    python = sys.executable
    os.execl(python, python, * sys.argv)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):

    auth = message.author

    if auth == client.user or message.author.bot: #obvious return is obvious
        return

    now = datetime.today().strftime("%d/%m/%Y %H:%M:%S")
    authID = message.author.id
    msg = message.content
    msgID = message.id
    guild = message.guild
    guildID = message.guild.id
    cn = message.channel
    cnName = message.channel.name
    cnID = message.channel.id
    coolMsgIDs = str(guildID) + '.' + str(cnID) + '.' + str(msgID)

    if authID == 368780147563823114 and msg.lower() == 'ernie':
        await cn.send(spokesperson)
        return

    elif 'retard' in msg: #correct ratards
        await cn.send('*ratard')
        return

    elif any(word in msg for word in config.slursList) and any(word in str(message.guild.id) for word in config.guildOptIn): #detect slurs & make them only work in whichever servers have opted in
        print('loser detected')
        await cn.send('loser ' + message.author.mention)
        return

    elif msg.startswith('ratmin ') or msg == 'ratmin' or msg == 'ratmint':#non functioning ratmin commands
        print(f'[{now}] ratmin in #{cnName} of {str(guild)} ({coolMsgIDs})')
        if authID == config.ratminID:
            if msg == 'ratmin sendhere':#don't bother getting this to work
                await cn.send(notFunctional)
            else:
                await cn.send('bruh that\'s not a command')
                return
        else:#if someone isn't ratmin, tell them to shut up
            await cn.send(random.choice(config.shutUp))
            return
    elif msg == 'ratstart' and authID == config.ratminID:
        restart()
    elif msg.startswith('rat'):#respond to rat with rat
        print(f'[{now}] rat in #{cnName} of {str(guild)} ({coolMsgIDs})')
        await cn.send('rat')
        return
    else:
#       print('else reached; message is ' + msg) #for debugging
        return

client.run(config.TOKEN)
