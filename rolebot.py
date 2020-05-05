import discord
import asyncio

TOKEN = 'bot token goes here'
client = discord.Client()
error = 'something has gone wrong, let <@302956027656011776> know>'
RoleName = 'RatBot Official Cool Role'
ratminID = 302956027656011776


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):

    user = message.author
    msg = message.content
    guild = message.guild
    userID = message.author.id

    if user == client.user or message.author.bot:
        return
    elif msg == 'give me the role, rat':
        if userID != ratminID:
            await message.channel.send('shut up ' + message.author.mention)
            print(str(user) + ' tried to role lol')
            return
        elif userID == ratminID:
            await message.channel.send('sure thing')
            await guild.create_role(name=RoleName)
            role = discord.utils.get(guild.roles, name=RoleName)
            await user.add_roles(role)
            return
        else:
            await message.channel.send(error)
    elif msg == 'you may leave now, rat' or msg == 'rat, fuck off':
        if userID != ratminID:
            await message.channel.send('shut up ' + message.author.mention)
            print(str(user) + ' tried to make me leave ' + str(guild) + ' lol')
            return
        elif message.author.id == ratminID:
            await message.channel.send('sure thing')
            await guild.leave()
        else:
            await message.channel.send(error)



client.run(TOKEN)
