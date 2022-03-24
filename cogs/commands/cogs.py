import re
from json import dump
from typing import Optional

from discord.ext import commands
from utils import FlagConverter, RatBot, RatCog


class Cogs(RatCog):
    all_extensions: list[str]
    # TODO: Combine repeated functions

    async def _on_ready(self):
        self.all_extensions = list(self.bot.extensions.keys())

    def dump_extensions(self):
        self.all_extensions = list(self.bot.extensions.keys())
        self.all_extensions.sort(key=lambda i: i.lower())
        with open("enabled_extensions.json", "w", encoding="utf-8") as file:
            dump(self.all_extensions, file)

    @staticmethod
    def trim_whitespace(string: str) -> str:
        return "".join(string.split())

    @commands.group(invoke_without_command=True, aliases=["c"])
    async def cogs(self, ctx: commands.Context):
        """Return cog list

        Subcommands load, unload, and reload cogs
        """
        await ctx.send(f"Loaded extensions: `{'`, `'.join(self.bot.extensions.keys())}`")

    @cogs.command(aliases=["l"])
    @commands.is_owner()
    async def load(self, ctx: commands.Context, tag: Optional[FlagConverter] = {}, *, params: str):
        """Load given cog(s)"""
        if params == "*":
            extensions = self.all_extensions
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
        self.dump_extensions()

    @cogs.command(aliases=["u"])
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, tag: Optional[FlagConverter] = {}, *, params: str):
        """Unload given cog(s)"""
        if params == "*":
            extensions = self.all_extensions
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
        self.dump_extensions()

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
        self.dump_extensions()


def setup(bot: RatBot):
    bot.add_cog(Cogs(bot))
