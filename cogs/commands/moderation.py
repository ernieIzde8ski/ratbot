import asyncio
import re
from typing import Callable

from discord import Message
from discord.ext import commands
from utils import FlagConverter, RatBot, RatCog


PruneChecks: dict[str, Callable[..., bool]] = {
    "ignore-humans": lambda msg, value: bool(msg.author.bot),
    "ignore-bots": lambda msg, value: not msg.author.bot,
    "ignore-webhooks": lambda msg, value: not msg.webhook_id,
    "attachments": lambda msg, value: bool(msg.attachments),
    "embeds": lambda msg, value: bool(msg.embeds),
    "plaintext": lambda msg, value: not msg.attachments and not msg.embeds,
    "match": lambda msg, value: bool(re.search(value, msg.content)),
}


class Moderation(RatCog):
    """Just a prune command, at the moment"""

    @staticmethod
    def get_check(flags: dict, msg: Message) -> Callable[[Message], bool]:
        if not flags:
            return lambda _msg: _msg != msg
        else:

            def check(msg: Message) -> bool:
                if msg == msg:
                    return False
                for check in PruneChecks:
                    value = flags[check]
                    if not PruneChecks[check](msg, value):
                        return False
                else:
                    return True

            return check

    @commands.command(aliases=["prune", "mass_delete"])
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx: commands.Context, amount: int = 50, *, flags: FlagConverter = {}):
        """Delete n messages en masse, with flags as parameters

        Valid flags: --ignore-humans, --ignore-bots, --ignore-webhooks,
                     --attachments, --embeds, --plaintext, --match <regex>
        All flags with dashes can be written alternatively with
        underscores (i.e. "--ignore_humans")
        """
        check = self.get_check(flags, ctx.message)
        await ctx.channel.purge(limit=amount, check=check)
        await ctx.message.add_reaction("☑️")
        await asyncio.sleep(2)
        await ctx.message.delete()


def setup(bot: RatBot):
    bot.add_cog(Moderation(bot))
