import re
from json import dump
from typing import Iterable, Optional

from discord.ext import commands
from utils import FlagConverter, RatCog


class Cogs(RatCog):
    # TODO: Combine repeated functions
    all_exts: Iterable[str]

    async def _on_ready(self):
        self.bot.config.enabled_extensions = set(self.bot.extensions.keys())
        self.all_exts = self.bot.config.enabled_extensions

    def save(self):
        self.bot.config.enabled_extensions = set(self.bot.extensions.keys())
        self.all_exts = self.bot.config.enabled_extensions
        self.bot.config.save()

    @staticmethod
    def trim_whitespace(string: str) -> str:
        return "".join(string.split())

    @commands.group(invoke_without_command=True, aliases=["c"])
    async def cogs(self, ctx: commands.Context):
        """Return cog list

        Subcommands load, unload, and reload cogs
        """
        await ctx.send(f"Loaded extensions: `{'`, `'.join(self.bot.extensions.keys())}`")

    @cogs.command(name="save", aliases=["s"])
    @commands.is_owner()
    async def _save(self, ctx: commands.Context):
        """Calls the Cogs.save() function"""
        self.save()
        await ctx.send("Saved enabled cogs!")
        print(f"Saved enabled cogs: {self.all_exts}")

    @cogs.command(aliases=["l"])
    @commands.is_owner()
    async def load(self, ctx: commands.Context, tag: Optional[FlagConverter] = {}, *, params: str):
        """Load given cog(s)"""
        if params == "*":
            extensions = self.all_exts
        else:
            extensions = re.split(r", *", params)
            extensions.sort()
        resp = ""
        for extension in extensions:
            try:
                self.bot.load_extension(extension)
            except (commands.ExtensionError, ModuleNotFoundError) as error:
                resp += f"{error.__class__.__name__}: {error}\n"
            else:
                resp += f"Loaded extension: {extension}\n"
        resp = "```\n" + resp.strip() + "\n```"
        print(resp)
        await ctx.send(resp)
        if tag.get("t") or tag.get("temporary"):
            return
        self.save()

    @cogs.command(aliases=["u"])
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, tag: Optional[FlagConverter] = {}, *, params: str):
        """Unload given cog(s)"""
        if params == "*":
            extensions = self.all_exts
        else:
            extensions = re.split(r", *", params)
            extensions.sort()
        resp = ""
        for extension in extensions:
            try:
                self.bot.unload_extension(extension)
            except (commands.ExtensionError, ModuleNotFoundError) as error:
                resp += f"{error.__class__.__name__}: {error}\n"
            else:
                resp += f"Unloaded extension: {extension}\n"
        resp = "```\n" + resp.strip() + "\n```"
        print(resp)
        await ctx.send(resp)
        if tag.get("t") or tag.get("temporary"):
            return
        self.save()

    @cogs.command(aliases=["r"])
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, tag: Optional[FlagConverter] = {}, *, params: str):
        """Reload given cog(s)"""
        if params == "*":
            extensions = list(self.bot.extensions.keys())
        else:
            extensions = re.split(r", *", params)
        extensions.sort()
        resp = ""
        for extension in extensions:
            try:
                self.bot.reload_extension(extension)
            except (commands.ExtensionError, ModuleNotFoundError) as error:
                resp += f"{error.__class__.__name__}: {error}\n"
            else:
                resp += f"Reloaded extension: {extension}\n"
        resp = "```\n" + resp.strip() + "\n```"
        print(resp)
        await ctx.send(resp)
        if tag.get("t") or tag.get("temporary"):
            return
        self.save()


setup = Cogs.basic_setup
