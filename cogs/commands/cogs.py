from modules.converters import FlagConverter
from typing import Optional
from json import dump
from discord.ext import commands


class Cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.all_extensions = []
        bot.loop.create_task(self.initialize())
    
    async def initialize(self):
        self.all_extensions = list(self.bot.extensions.keys())

    async def dump_extensions(self):
        self.all_extensions = list(self.bot.extensions.keys())
        with open("enabled_extensions.json", "w", encoding="utf-8") as file:
            dump(self.all_extensions, file)

    @staticmethod
    def trim_whitespace(string: str):
        return ''.join(string.split())

    @commands.group(invoke_without_command=True, aliases=["c"])
    async def cogs(self, ctx):
        await ctx.send(f"Loaded extensions: `{'`, `'.join(self.bot.extensions.keys())}`")

    @cogs.command(aliases=["l"])
    async def load(self, ctx, tag: FlagConverter = {}, *, extensions: Optional[str]):
        if not extensions: await ctx.send("No parameter was given") ; return
        if extensions == "*":
            extensions = self.all_extensions
        else:
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
        if tag.get("t") or tag.get("temporary"): return
        await self.dump_extensions()

    @cogs.command(aliases=["u"])
    async def unload(self, ctx, tag: FlagConverter = {}, *, extensions: Optional[str]):
        if not extensions: await ctx.send("No parameter was given") ; return
        if extensions == "*":
            extensions = self.all_extensions
        else:
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
    
    @cogs.command(aliases=["r"])
    async def reload(self, ctx, *, extensions: Optional[str]):
        if not extensions: await ctx.send("No parameter was given") ; return
        if extensions == "*":
            extensions = list(self.bot.extensions.keys())
        else:
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
