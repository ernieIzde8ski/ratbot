from datetime import datetime
import random
from typing import Optional, Union
from urllib.parse import quote_plus

import discord
import discord.ext.commands as commands


def birthdaylink(name):
    return f"https://itsyourbirthday.today/#{quote_plus(name)}"


def now():
    return str(datetime.today().strftime("%d-%m-%Y %H:%M:%S"))


async def log(bot, msg: str):
    channel = bot.get_channel(762166605458964510)
    await channel.send(content=msg)


def b(x):
    if x > 104:
        return "To Much Bro"
    else:
        return f"""Bro.... Liking {'"Liking ' * x}Things {'Is Cringe" ' * x}is Cringe...."""


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["bM", "bm"])
    async def bM_meter(self, ctx, *, option: Optional[str]):
        """decides Based or Cringe"""
        option = option.replace("```", "Armenium") if option else 'Your'
        random.seed(option)
        BC_decision = random.choice(["Based", "Cringe"]) if option else "Cringe"
        punctuation_ending = random.choice([random.choice(("!", ".")) * x for x in range(1, 8)])

        await ctx.send(content=(f"**{option}** are **{BC_decision}**{punctuation_ending}"))
        await log(self.bot, "```"
                            f"{option}, {BC_decision}{punctuation_ending}   [{ctx.message.created_at}]"
                            "```")

    @commands.command(aliases=["time", "now", "EST", "est"])
    async def based_time(self, ctx):
        """Tells the Ernie Standard Time"""
        await ctx.send(f"it\'s {now()} in EST (Ernie Standard Time)")
        return

    @commands.command(aliases=["CC", "cc"])
    async def cringecount(self, ctx, iteration: int = 1):
        """\"Liking liking things is cringe is cringe\""""
        try:
            await ctx.send(b(iteration))
        except:
            await ctx.send("Yo Did it Wrong Bro")

    @commands.command(aliases=["bd"])
    async def birthday(self, ctx, recipient: Union[discord.Member, str], *, name: Optional[str]):
        if not name:
            await ctx.channel.send("Cringe?")
            return
        if not isinstance(recipient, str) and not name:  # if the person is mentioned without additional name
            await ctx.channel.send(f"happy birthday {recipient.mention}! \n{birthdaylink(recipient.display_name)}")
        elif not isinstance(recipient, str) and name:  # if the person is mentioned with name
            await ctx.channel.send(f"happy birthday {recipient.mention}! \n{birthdaylink(name)}")
        elif isinstance(recipient, str) and not name:
            await ctx.channel.send(f"happy birthday {recipient}! \n{birthdaylink(recipient)}")
        elif isinstance(recipient, str) and name:
            await ctx.channel.send(f"happy birthday {recipient}! \n{birthdaylink(name)}")


def setup(bot):
    bot.add_cog(Fun(bot))
