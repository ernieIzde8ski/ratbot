from typing import Optional, Union
from random import choice, randint
from datetime import datetime
import discord
import discord.ext.commands as commands
from urllib.parse import quote_plus
import core.mentions as mentions

def birthdaylink(name):
    return f"https://itsyourbirthday.today/#{quote_plus(name)}"
def now():
    return str(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))
async def log(bot, msg: str):
    channel = bot.get_channel(762166605458964510)
    await channel.send(content = msg, allowed_mentions = discord.AllowedMentions.none())
def b(x):
    if x > 104:
        return "To Much Bro"
    else:
        return (f"""Bro.... Liking {'"Liking '*x}Things {'Is Cringe" '*x}is Cringe....""")


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ["bM", "bm"])
    async def bM_meter(self, ctx, *, option: Optional[str]):
        """decides Based or Cringe"""
        BC_decision = choice(["Based", "Cringe"]) if option else "Cringe"
        punctuation_ending = choice([choice(("!", ".")) * x for x in range(1, 8)])
        option = option.replace("```", "Armenium") if option else 'Your'

        await ctx.send(content=(f"**{option}** are **{BC_decision}**{punctuation_ending}"), allowed_mentions=discord.AllowedMentions.none())
        await log(self.bot, "```"
        f"{option}, {BC_decision}{punctuation_ending}   [{ctx.message.created_at}]"
        "```")

    @commands.command(aliases = ["time", "now", "EST", "est"])
    async def based_time(self, ctx):
        """Tells the Ernie Standard Time"""
        await ctx.send(f"it\'s {now()} in EST (Ernie Standard Time)")
        return

    @commands.command(aliases = ["CC", "cc"])
    async def cringecount(self, ctx, iteration: int = 1):
        """\"Liking liking things is cringe is cringe\""""
        try:
            await ctx.send(b(iteration))
        except:
            await ctx.send("Yo Did it Wrong Bro")

    @commands.command(aliases=["bd"])
    async def birthday(self, ctx, recipient: Union[commands.MemberConverter, str], *, name: Optional[str]):
        if name == False:
            await ctx.channel.send("Cringe?")
            return
        if not isinstance(recipient, str) and not name: #if the person is mentioned without additional name
            await ctx.channel.send(f"happy birthday {recipient.mention}! \n{birthdaylink(recipient.display_name)}", allowed_mentions=mentions.none)
        elif not isinstance(recipient, str) and name:     #if the person is mentioned with name
            await ctx.channel.send(f"happy birthday {recipient.mention}! \n{birthdaylink(name)}", allowed_mentions=mentions.none)
        elif isinstance(recipient, str) and not name:
            await ctx.channel.send(f"happy birthday {recipient}! \n{birthdaylink(recipient)}", allowed_mentions=mentions.none)
        elif isinstance(recipient, str) and name:
            await ctx.channel.send(f"happy birthday {recipient}! \n{birthdaylink(name)}", allowed_mentions=mentions.none)
def setup(bot):
    bot.add_cog(Fun(bot))
