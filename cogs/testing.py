from typing import Optional, Union
from datetime import datetime
import discord
import discord.ext.commands as commands
from time import sleep
import asyncio

def printList(list):
    for x in range(len(list)):
        print(list[x])
def predicate(message):
    if message.author.id == 466737001832382464:
        return True
    else:
        return False
async def spammy(messageable, phrase):
    await messageable.send(phrase)
    await asyncio.sleep(1.5)

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def spam(self, ctx, phrase: str, mode: Optional[str], count: Optional[int]):
        if mode:
            if mode == "time":
                await ctx.channnel.send("no")
            elif mode == "loop":
                if count == -1:
                    while True:
                        await spammy(ctx.channel, phrase)
                else:
                    for i in range(0, count):
                        await spammy(ctx.channel, phrase)
        else:
            while True:
                await spammy(ctx.channel, phrase)

    @commands.command()
    @commands.is_owner()
    async def channelperms(self, ctx):
        for channel in ctx.guild.channels:
            for i in channel.overwrites:
                await channel.set_permissions(i, overwrite=None, reason="Yes")
        await ctx.channel.send("Finished")

    @commands.command()
    @commands.is_owner()
    async def roleperms(self, ctx):
        for i in ctx.guild.roles:
            await i.edit(permissions=discord.Permissions.none(), reason="Yes")
        await ctx.channel.send("Finished")

    @commands.command()
    @commands.is_owner()
    async def zeros(self, ctx):
        """doesnt work because of intents"""
        a = []
        for role in ctx.guild.roles:
            if len(role.members) == 0:
                a.append(role.name)
            print(f"{len(role.members)}, {role.name}")
        await ctx.channel.send(a, allowed_mentions=discord.AllowedMentions.none())

    @commands.command()
    @commands.is_owner()
    async def purge(self, ctx):
        """deletes roles in the list and prints their hex id"""
        namelist = ["LEWD SATAN", "noogie god", "Maximum Foxxo", "Paradox Meme", "TheSmol", "Everyone and Everything", "That One Child", "Jew of Mew say Awoo", "Online?", "former god", "Clowns for Jesus", "The Backwards Bois", "band", "gay baby", "what the fuck", "shUT THEF FUCK UP", "Chicken Man", "clonck gay", "Pervy Bard", "Cracker-Obsessed Loon"]
        guildlist = ctx.guild.roles
        for rolename in namelist:
            for role in ctx.guild.roles:
                if role.name == rolename:
                    print(f"{role.name}, {role.color}")
                    await role.delete()

    @commands.command()
    @commands.is_owner()
    async def channelList(self, ctx):
        await ctx.channel.send(str(ctx.guild.text_channels))
    @commands.command()
    @commands.is_owner()
    async def bargeinto(self, ctx, *, channel: commands.TextChannelConverter):
        await ctx.channel.send("ok lemme try")
        try:              await channel.set_permissions(ctx.author, read_messages=True, send_messages=True, read_message_history=True)
        except discord.Forbidden: await ctx.channel.send("Mission Failed: Denied")
        except:           await ctx.channel.send("Mission Failed")
        else:             await ctx.channel.send("Mission Suceed?")

    @commands.command()
    @commands.is_owner()
    async def rat_history(self, ctx, *, cap: Optional[int]):
        """get rats in channel history"""

        messages = await ctx.channel.history(limit=(cap if cap else 1400)).filter(predicate).flatten()
        for m in messages:
            if '** are **' in m.content:  print(m.content.replace("**", "").replace(" are ", ", ") + f"[{m.created_at}]")


def setup(bot):
    bot.add_cog(Fun(bot))
