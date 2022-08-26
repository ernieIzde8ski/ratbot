from functools import cached_property
import logging
import traceback
from typing import Any, Callable

from discord.ext import commands
from settings import _enabled_extensions_factory, settings
from utils import RatCog, RatCtx, codeblock


class ExtensionHandling(RatCog):
    if settings.debug is True:

        async def on_ready_hook(self):
            exts = ", ".join(self.bot.extensions)
            logging.info(f"Loaded extensions: {exts}")

    @cached_property
    def ext_key(self):
        return next(
            k for k, v in self.bot.extensions.items() if type(self).__name__ in v.__dict__
        )

    @commands.is_owner()
    @commands.hybrid_group(aliases=("exts", "e"))
    async def extensions(self, ctx: RatCtx) -> None:
        """Display extensions"""
        loaded_extensions = sorted(self.bot.extensions)
        settings.enabled_extensions.sort()
        loaded = "`" + "`, `".join(self.bot.extensions) + "`"
        if loaded_extensions == settings.enabled_extensions:
            await ctx.channel.send(f"Loaded extensions: {loaded}")
        else:
            enabled = "`" + "`, `".join(settings.enabled_extensions) + "`"
            await ctx.channel.send(
                f"Loaded extensions: {loaded}\nEnabled extensions: {enabled}"
            )

    @commands.is_owner()
    @extensions.command(aliases=("l",))
    async def load(self, ctx: RatCtx, *, args: str = "*"):
        """Load extensions

        If * or no argument is passed, load every non-loaded file in `cogs/`.
        """
        # obtain extensions to iterate over
        exts = (
            [
                ext
                for ext in _enabled_extensions_factory()
                if ext not in self.bot.extensions
            ]
            if args == "*"
            else args.split()
        )
        if not exts:
            raise RuntimeError("There's nothing to Load !")
        # handle extensions
        # this chunk is roughly identical to the other subcommands
        resp = f"Loading: {exts}\n\n" if len(exts) != 1 else ""
        for ext in exts:
            try:
                await self.bot.load_extension(ext)
                resp += f"Loaded: {ext}\n"
            except Exception as err:
                err_text = "".join(traceback.format_exception(err))
                err_text = codeblock(err_text, lang="py")
                await ctx.send(f"Extension failed: {ext}\n{err_text}")
                resp += f"Failed: {ext}\n"
        # send message
        await ctx.send(codeblock(resp))

    @commands.is_owner()
    @extensions.command(aliases=("r",))
    async def reload(self, ctx: RatCtx, *, args: str = "*"):
        # obtain extensions
        exts = list(self.bot.extensions) if args == "*" else args.split()
        # handle extensions
        resp = f"Reloading: {exts}\n\n" if len(exts) != 1 else ""
        for ext in exts:
            try:
                await self.bot.reload_extension(ext)
                resp += f"Reloaded: {ext}\n"
            except Exception as err:
                err_text = "".join(traceback.format_exception(err))
                err_text = codeblock(err_text, lang="py")
                await ctx.send(f"Extension failed: {ext}\n{err_text}")
                resp += f"Failed: {ext}\n"
        # send message
        await ctx.send(codeblock(resp))

    @commands.is_owner()
    @extensions.command(aliases=("u",))
    async def unload(self, ctx: RatCtx, *, args: str = "*"):
        # obtain extensions
        exts = (
            # disallow implicitly unloading this class itself
            [ext for ext in self.bot.extensions if ext != self.ext_key]
            if args == "*"
            else args.split()
        )
        if not exts:
            raise RuntimeError("There's nothing to Unload !")
        # handle extensions
        resp = f"Unloading: {exts}\n\n" if len(exts) != 1 else ""
        for ext in exts:
            try:
                await self.bot.unload_extension(ext)
                resp += f"Unloaded: {ext}\n"
            except Exception as err:
                err_text = "".join(traceback.format_exception(err))
                err_text = codeblock(err_text, lang="py")
                await ctx.send(f"Extension failed: {ext}\n{err_text}")
                resp += f"Failed: {ext}\n"
        # send message
        await ctx.send(codeblock(resp))


setup = ExtensionHandling.basic_setup
