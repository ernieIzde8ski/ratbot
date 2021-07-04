from discord.ext import commands


class ErrorHandling(commands.Cog):
    def __init__(self):
        pass

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if ctx.prefix == "" and isinstance(error, commands.CommandNotFound):
            return
        await ctx.reply(f"{error.__class__.__name__}: {error}")


def setup(bot):
    bot.add_cog(ErrorHandling())
