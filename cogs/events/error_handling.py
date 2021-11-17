from discord.ext import commands
from fuzzywuzzy import fuzz


class ErrorHandling(commands.Cog):
    def __init__(self):
        pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if ctx.prefix == "" and isinstance(error, commands.CommandNotFound):
            return
        elif ctx.command:
            if ctx.command.has_error_handler():
                return

        resp = f"{error.__class__.__name__}: {error}\n"
        # Show the closest matching command if the error is CommandNotFound.
        if isinstance(error, commands.CommandNotFound):
            # Generate command name list, with aliases included.
            cmds = list(map(lambda cmd: cmd.name.lower(), ctx.bot.commands))
            aliases = list(map(lambda cmd: cmd.aliases, ctx.bot.commands))
            aliases = [item for elem in aliases for item in elem]
            cmds += aliases
            cmds.sort(key=lambda cmd: fuzz.ratio(ctx.invoked_with.lower(), cmd), reverse=True)
            resp += f"Closest match: `{cmds[0]}`."
        await ctx.reply(resp)


def setup(bot):
    bot.add_cog(ErrorHandling())
