import traceback
from typing import TYPE_CHECKING

from discord.ext import commands
from fuzzywuzzy import fuzz
from settings import channels
from utils import RatCog, RatCtx, codeblock


def similar_string_sort(string: str):
    string = string.lower()

    def key(item: str):
        return fuzz.ratio(item.lower(), string)

    return key


def format_exception(exc: Exception):
    return "".join(traceback.format_exception(exc))


# textwrap.shorten didn't really work here - it replaces all line endings with spaces
def shorten(string: str, width: int, final_line: str = "[...]") -> str:
    """Truncate a string on a line-by-line basis."""
    res = ""
    for line in string.splitlines():
        if (len(res) + len(line)) > width:
            res += final_line
            break
        res += line + "\n"
    return res


class ErrorHandling(RatCog):
    ignored_exceptions = commands.CommandNotFound | commands.NotOwner
    """Exceptions not worth logging."""

    @commands.Cog.listener()
    async def on_command_error(self, ctx: RatCtx, err: commands.CommandError):
        if ctx.command and ctx.command.has_error_handler():
            return  # no use in handling errors twice

        # notify user of error
        resp = f"{type(err).__name__}: {err}\n"
        # match closest command if CommandNotFound is raised
        if isinstance(err, commands.CommandNotFound):
            if TYPE_CHECKING:
                assert ctx.invoked_with
            cmds = [cmd.name.lower() for cmd in self.bot.commands]
            aliases = [
                i.lower() for j in (cmd.aliases for cmd in self.bot.commands) for i in j
            ]
            cmds += aliases
            cmds.sort(key=similar_string_sort(ctx.invoked_with))
            resp += f"Closest match: `{cmds[-1]}`\n"
        await ctx.reply(resp)

        # avoid logging certain errors
        if isinstance(err, self.ignored_exceptions):
            return

        # log any other error to errors channel
        exc_tb = shorten(format_exception(err), width=1900)
        resp = "An exception occurred:\n" + codeblock(
            f"Guild:   {f'{ctx.guild.id} | {ctx.guild}' if ctx.guild else None}\n"
            f"Channel: {ctx.channel.id} | {ctx.channel}\n"
            f"User:    {ctx.author.id} | {ctx.author}\n"
            "\n--------\n\n" + exc_tb
        )
        await channels.errors.send(resp)


setup = ErrorHandling.basic_setup
