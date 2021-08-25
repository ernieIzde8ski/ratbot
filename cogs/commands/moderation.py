from asyncio import sleep
from discord.ext import commands
from discord import Message

from modules.converters import FlagConverter
import re


class Moderation(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.checks = {
            "ignore-humans": lambda msg, value: msg.author.bot,
            "ignore-bots": lambda msg, value: not msg.author.bot,
            "ignore-webhooks": lambda msg, value: not msg.webhook_id,
            "attachments": lambda msg, value: msg.attachments,
            "embeds": lambda msg, value: msg.embeds,
            "plaintext": lambda msg, value: not msg.attachments and not msg.embeds,
            "match": lambda msg, value: re.search(value, msg.content)
        }

    @commands.command(aliases=["prune", "mass_delete"])
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: int = 50, *, flags: FlagConverter = {}):
        """Delete n messages en masse, with flags as parameters
        
        Valid flags: --ignore-humans, --ignore-bots, --ignore-webhooks,
                     --attachments, --embeds, --plaintext, --match <regex>
        All flags with dashes can be written alternatively with
        underscores (i.e. "--ignore_humans")
        """
        if not flags:
            def check(msg): return msg != ctx.message
        else:
            flags = {key.lower().replace("_", "-"): value for key, value in flags.items()}
            checks = [check for check in self.checks if check in flags]
            def check(msg: Message) -> bool:
                if msg == ctx.message:
                    return False
                for check in checks:
                    value = flags[check]
                    if not self.checks[check](msg, value):
                        return False
                else:
                    return True
    
        await ctx.channel.purge(limit=amount, check=check)
        await ctx.message.add_reaction("☑️")
        await sleep(2)
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Moderation(bot))
