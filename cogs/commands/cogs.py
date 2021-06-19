from modules.converters import FlagConverter
from typing import Optional
from json import dump
from discord.ext import commands


class Cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def dump_extensions(self):
        with open("enabled_extensions.json", "w", encoding="utf-8") as file:
            dump(list(self.bot.extensions.keys()), file)

    @staticmethod
    def trim_whitespace(string: str):
        return ''.join(string.split())

    @commands.group(invoke_without_command=True)
    async def cogs(self, ctx):
        await ctx.send(f"Loaded extensions: `{'`, `'.join(self.bot.extensions.keys())}`")

    @cogs.command()
    async def load(self, ctx, *, extensions: Optional[str]):
        if not extensions: await ctx.send("No parameter was given") ; return
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
        print(resp); await ctx.send(resp)
        await self.dump_extensions()

    @cogs.command()
    async def unload(self, ctx, tag: FlagConverter = {}, *, extensions: Optional[str]):
        if not extensions: await ctx.send("No parameter was given") ; return
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
        print(resp); await ctx.send(resp)
        if tag.get("t") or tag.get("temporary"): return
        await self.dump_extensions()
    
    @cogs.command()
    async def reload(self, ctx, *, extensions: Optional[str]):
        if not extensions: await ctx.send("No parameter was given") ; return
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
        print(resp); await ctx.send(resp)

def setup(bot):
    bot.add_cog(Cogs(bot))
