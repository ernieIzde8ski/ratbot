import logging
import traceback
from typing import Callable

from disnake.ext import commands
from disnake.ext.commands import (
    ExtensionAlreadyLoaded,
    ExtensionNotFound,
    ExtensionNotLoaded,
    NotOwner,
    UserInputError,
)

from lib.bot import Cog, CommandError, Interaction
from lib.converters import CommaList

ERROR_LOG_FORMAT = """
```
{contents}
```
Feel free to report this to @{owner} Lol
"""


class Cogs(Cog):
    async def ext_command_handler(
        self,
        inter: Interaction,
        func: Callable[[str], None],
        action: str,
        exts: list[str],
    ) -> None:
        if not exts:
            raise UserInputError(f"couldn't figure out which extensions to {action}")

        await inter.send(
            f"{action} extensions . . .", ephemeral=self.settings.hide_mod_commands
        )

        failed = 0
        total = len(exts)

        log = "```\n"

        for ext in exts:
            try:
                func(ext)
            except Exception as exc:
                failed += 1
                msg = (
                    f"Failed to {action} extension '{ext}':\n"
                    f"\t{type(exc).__name__}: {exc}"
                )

                # some exceptions are not worth looking at in the console
                if not isinstance(
                    exc, (ExtensionAlreadyLoaded, ExtensionNotLoaded, ExtensionNotFound)
                ):
                    logging.exception(msg)
            else:
                msg = f"Managed to {action} extension '{ext}'"
                logging.debug(msg)

            log += msg
            log += "\n"

        if failed == 0:
            final_log = f"All extensions {action}ed successfully!"
        else:
            ratio = failed * 10_000 // total / 100
            final_log = f"{ratio}% of extensions failed to {action}."

        logging.debug(final_log)
        await inter.edit_original_response(log + "```\n" + final_log)

    @commands.slash_command()
    @commands.is_owner()
    async def load_extensions(
        self, inter: Interaction, extensions: list[str] = CommaList()
    ) -> None:
        """Loads given extensions."""
        await self.ext_command_handler(inter, self.bot.load_extension, "load", extensions)

    @commands.slash_command()
    @commands.is_owner()
    async def reload_extensions(
        self, inter: Interaction, extensions: list[str] = CommaList()
    ) -> None:
        """Reloads given extensions. If none are given, defaults to all."""
        extensions = extensions or list(self.bot.extensions)
        await self.ext_command_handler(
            inter, self.bot.reload_extension, "reload", extensions
        )

    @commands.slash_command()
    @commands.is_owner()
    async def unload_extensions(
        self, inter: Interaction, extensions: list[str] = CommaList()
    ) -> None:
        """Unloads given extensions."""
        await self.ext_command_handler(
            inter, self.bot.reload_extension, "unload", extensions
        )

    @Cog.listener()
    async def on_slash_command_error(
        self, inter: Interaction, error: CommandError
    ) -> None:
        if isinstance(error, NotOwner | UserInputError):
            msg = type(error).__name__ + " error: " + str(error)
            await inter.send(msg)
        else:
            msg = "\n".join(traceback.format_exception(error))

            if len(msg) > 1950:
                index = msg.rfind("\n", 0, 1950)
                msg = msg[:index] + "\n..."

            msg = ERROR_LOG_FORMAT.format(contents=msg, owner=self.app_info.owner)
            await inter.send(msg, ephemeral=True)
