from discord.ext import commands


class Cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def trim_whitespace(string: str):
        return ''.join(string.split())

    @commands.group(invoke_without_command=True)
    async def cogs(self, ctx):
        await ctx.send(f"Loaded extensions: `{'`, `'.join(self.bot.extensions.keys())}`")

    @cogs.command()
    async def load(self, ctx, *, extensions: str):
        extensions = self.trim_whitespace(extensions).split(",")
        resp = ""
        for extension in extensions:
            try:
                self.bot.load_extension(extension)
            except commands.ExtensionError as error:
                resp += f"{error.__class__.__name__}: {error}\n"
            except ModuleNotFoundError as error:
                resp += f"{error.__class__.__name__}: {error}\n"
            else:
                resp += f"Loaded extension: {extension}\n"
        resp = resp.strip()
        print(resp) ; await ctx.send(resp)
    
    @cogs.command()
    async def unload(self, ctx, *, extensions: str):
        extensions = self.trim_whitespace(extensions).split(",")
        resp = ""
        for extension in extensions:
            try:
                self.bot.unload_extension(extension)
            except commands.ExtensionError as error:
                resp += f"{error.__class__.__name__}: {error}\n"
            except ModuleNotFoundError as error:
                resp += f"{error.__class__.__name__}: {error}\n"
            else:
                resp += f"Unloaded extension: {extension}\n"
        resp = resp.strip()
        print(resp) ; await ctx.send(resp)
    
    @cogs.command()
    async def reload(self, ctx, *, extensions: str):
        extensions = self.trim_whitespace(extensions).split(",")
        resp = ""
        for extension in extensions:
            try:
                self.bot.reload_extension(extension)
            except commands.ExtensionError as error:
                resp += f"{error.__class__.__name__}: {error}\n"
            except ModuleNotFoundError as error:
                resp += f"{error.__class__.__name__}: {error}\n"
            else:
                resp += f"Reloaded extension: {extension}\n"
        resp = resp.strip()
        print(resp) ; await ctx.send(resp)

def setup(bot):
    bot.add_cog(Cogs(bot))
