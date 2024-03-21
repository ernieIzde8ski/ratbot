import logging
import traceback

from lib.bot import Bot, Cog, CommandError, Interaction, slash_command
from lib.converters import CommaList

ERROR_LOG_FORMAT = """
```
{contents}
```
Feel free to report this to @{owner} Lol
"""


class Cogs(Cog):
    @slash_command()
    async def reload_exts(
        self, inter: Interaction, extensions: list[str] = CommaList()
    ) -> None:
        """
        Reloads given extensions.

        If no extensions are given, reloads all extensions.
        """
        await inter.send(
            "Reloading extensions . . .", ephemeral=self.settings.hide_mod_commands
        )

        if not extensions:
            extensions = list(self.bot.extensions)
        logging.info(f"{extensions}")

        failed = 0
        total = len(extensions)

        log = "```\n"

        for ext in extensions:
            try:
                self.bot.reload_extension(ext)
            except Exception as exc:
                m = (
                    f"Failed to reload extension '{ext}':\n"
                    f"\t{type(exc).__name__}: {exc}"
                )
                logging.exception(m)
                failed += 1
            else:
                m = f"Managed to reload extension '{ext}'"
                logging.debug(m)
            log += m
            log += "\n"

        if failed == 0:
            final_log = "All extensions reloaded successfully!"
        else:
            ratio = failed * 10_000 // total / 100
            final_log = f"{ratio}% of extensions failed to reload."

        logging.debug(final_log)
        await inter.edit_original_response(log + "```\n" + final_log)

    @Cog.listener()
    async def on_slash_command_error(
        self, inter: Interaction, error: CommandError
    ) -> None:
        msg = "\n".join(traceback.format_exception(error))

        if len(msg) > 1950:
            index = msg.rfind("\n", 0, 1950)
            msg = msg[:index] + "\n..."

        msg = ERROR_LOG_FORMAT.format(contents=msg, owner=self.app_info.owner)

        await inter.send(msg, ephemeral=True)


def setup(bot: Bot) -> None:
    bot.add_cog(Cogs(bot))
