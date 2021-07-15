from discord.ext import commands
from fuzzywuzzy import fuzz


class ErrorHandling(commands.Cog):
    def __init__(self):
        pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if ctx.prefix == "" and isinstance(error, commands.CommandNotFound):
            return
        
        resp = f"{error.__class__.__name__}: {str(error).removesuffix('.')}.\n"
        if isinstance(error, commands.CommandNotFound):
            cmds = list(map(lambda cmd: cmd.name.lower(), ctx.bot.commands))
            cmds.sort(key=lambda cmd: fuzz.ratio(ctx.invoked_with.lower(), cmd), reverse=True)
            resp += f"Closest match: `{cmds[0]}`."
        await ctx.reply(resp)


def setup(bot):
    bot.add_cog(ErrorHandling())
