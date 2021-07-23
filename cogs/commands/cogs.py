from discord.ext import commands
from json import dump

import re
from typing import Optional

from modules.converters import FlagConverter


class Cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.all_extensions = []
        bot.loop.create_task(self.initialize())

    async def initialize(self):
        await self.bot.wait_until_ready()
        self.all_extensions = list(self.bot.extensions.keys())

    async def dump_extensions(self):
        self.all_extensions = list(self.bot.extensions.keys())
        self.all_extensions.sort(key=lambda i: i.lower())
        with open("enabled_extensions.json", "w", encoding="utf-8") as file:
            dump(self.all_extensions, file)

    @staticmethod
    def trim_whitespace(string: str) -> str:
        return ''.join(string.split())

    @commands.command(aliases=["uc", "cmd", "command"])
    @commands.is_owner()
    async def update_command(self, ctx, command_name: str, *, flags: FlagConverter = {}):
        """Update a command's attributes"""
        try:
            cmd = list(filter(
                lambda cmd: command_name.lower(
                ) in cmd.aliases or command_name == cmd.name, self.bot.commands
            ))[0]
        except IndexError:
            raise commands.BadArgument(
                "Converting to command failed for parameter \"command_name\"."
            )
        else:
            cmd.update(**flags)
            await ctx.send(f"Updated command `{cmd.name}`")

    @commands.group(invoke_without_command=True, aliases=["c"])
    async def cogs(self, ctx):
        """Return cog list

        Subcommands load, unload, and reload cogs
        """
        await ctx.send(f"Loaded extensions: `{'`, `'.join(self.bot.extensions.keys())}`")

    @cogs.command(aliases=["l"])
    @commands.is_owner()
    async def load(self, ctx, tag: Optional[FlagConverter] = {}, *, extensions: str):
        """Load given cog(s)"""
        if extensions == "*":
            extensions = self.all_extensions
        else:
            extensions = re.split(r", *", extensions)
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
        await self.dump_extensions()

    @cogs.command(aliases=["u"])
    @commands.is_owner()
    async def unload(self, ctx, tag: Optional[FlagConverter] = {}, *, extensions: str):
        """Unload given cog(s)"""
        if extensions == "*":
            extensions = self.all_extensions
        else:
            extensions = re.split(r", *", extensions)
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
        await self.dump_extensions()

    @cogs.command(aliases=["r"])
    @commands.is_owner()
    async def reload(self, ctx, tag: Optional[FlagConverter] = {}, *, extensions: str):
        """Reload given cog(s)"""
        if extensions == "*":
            extensions = list(self.bot.extensions.keys())
        else:
            extensions = re.split(r", *", extensions)
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
        await self.dump_extensions()


def setup(bot):
    bot.add_cog(Cogs(bot))
