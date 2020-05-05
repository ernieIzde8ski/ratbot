# bot.py #i don't know what this does but it's here i guess
import os
import discord
import asyncio
from datetime import datetime
import random


TOKEN = 'put token here'

client = discord.Client()


def is_in(symbol, lst):
    return any(symbol in x for x in lst)


shutUp = ['shut up liberal', 'what do you want', 'i am your god who the hell do you think you are', 'wot', 'wut', 'WHAT DO YOU WANT', 'wot you want, pathetic mortal', 'lower your shields and surrender your ships because this is the end for your civilization', 'death to capitalism & you', 'do you have nothing better with your life to do right now', 'what', 'что', 'look i don\'t know what you think is a productive use of time but this is not it', 'how HIGH do you even have to BE', 'do you ever think of the utterly meaningless impact your messages right here will ever have', 'couldn\'t you be out there being productive rn', 'I DONT CARE ABOUT YOU', 'you look your best away from the keyboard; never forget', 'https://en.wikipedia.org/wiki/Shut_up', 'https://www.youtube.com/watch?v=KRB-iHGHSqk', 'https://www.youtube.com/watch?v=RwC9CP_2YKE', 'this is explicitly a bot admin command what do you want from me', '']
slursList = ['nigger', 'nigga', 'niga', 'negroid', 'jigaboo', 'cracker', 'faggot', 'fag', 'slut', 'whore', 'gook', 'ExampleSlur']
guildOptIn = ['488475203303768065', '682704934621282307']
notFunctional = 'this functional is not currently functional. please fix it soon eridan man'


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    coolMessageIDs = '(' + str(message.guild.id) + '.' + str(message.channel.id) + '.' + str(message.id) + ')'
    now = datetime.today()

    if message.author == client.user or message.author.bot: #obvious return is obvious
        return

    elif 'retard' in message.content: #correct ratards
        await message.channel.send('*ratard')
        return

    elif any(word in message.content for word in slursList) and any(word in str(message.guild.id) for word in guildOptIn): #detect slurs & make them only work in whichever servers have opted in
        print('loser detected')
        await message.channel.send('loser ' + message.author.mention)
        return

    elif message.content.startswith('ratmin ') or message.content == 'ratmin' or message.content == 'ratmint':#non functioning ratmin commands
        print('[' + now.strftime("%d/%m/%Y %H:%M:%S") + '] ratmin in #' + message.channel.name + ' of ' + str(message.guild) + ' ' + coolMessageIDs)
        if message.author.id == 302956027656011776:
            if message.content == 'ratmin sendhere':#don't bother getting this to work
                channel = message.channel
                await channel.send('say hello now')

                def check(m):
                    return m.content == 'hello' and m.channel == channel

                msg = await client.wait_for('message', check=check)
                await channel.send('hello {.author}!'.format(msg))
                return
            else:
                await message.channel.send('bruh that\'s not a command')
                return
        else:#if someone isn't ratmin, tell them to shut up
            await message.channel.send(random.choice(shutUp))
            return

    elif message.content == 'rat' or message.content == 'ratbot':#respond to rat with rat
        print('[' + now.strftime("%d/%m/%Y %H:%M:%S") + '] rat in #' + message.channel.name + ' of ' + str(message.guild) + ' ' + coolMessageIDs)
        respuesta = 'rat'
        await message.channel.send(respuesta)
        return

    else:
#       print('else reached; message is ' + message.content) #for debugging
        return

client.run(TOKEN)
