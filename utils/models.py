import logging
import traceback
from typing import Any, Callable, Coroutine

import discord
from discord.ext import commands
from settings import settings, channels, generate_extensions_list
from .extra import codeblock


def _format_exception(exc: Exception, /):
    return f"{type(exc).__name__}: {exc}\n\n" + "".join(traceback.format_exception(exc))


class RatBot(commands.Bot):
    def __init__(
        self,
        command_prefix: Callable[["RatBot", discord.Message], list[str]],
        allowed_mentions: discord.AllowedMentions = discord.AllowedMentions.none(),
        intents: discord.Intents = discord.Intents.all(),
        **kwargs: Any,
    ):
        super().__init__(
            command_prefix=command_prefix,
            allowed_mentions=allowed_mentions,
            intents=intents,
            **kwargs,
        )

    async def on_message(self, msg: discord.Message):
        # Message handling occurs before any command parsing
        if msg.author.bot or msg.author.id in settings.blocked:
            return
        elif str(msg.channel) == "rat":
            if msg.content == "rat":
                await msg.channel.send("rat")
            else:
                await msg.delete()
                return
        elif "rat" in msg.content.split():
            await msg.channel.send("rat")
        await self.process_commands(msg)

    async def on_ready(self):
        logging.info("I'm Alive my Friend ! (I can see the Shadows everywhere)")
        logging.info(f"i Am {self.user}")

    async def setup_hook(self) -> None:
        # make sure these channels get loaded eventually
        coro = channels.set_channels(self)
        self.loop.create_task(coro)

        # load enabled extensions
        # while programming, it is convenient to load *every* extension
        if settings.debug:
            settings.enabled_extensions += generate_extensions_list()
        settings.reduce_enabled_extensions()
        for ext in settings.enabled_extensions:
            try:
                await self.load_extension(ext)
                logging.info(f"Loaded extension: {ext}")
            except Exception as err:
                logging.critical(_format_exception(err))

        # make sure settings are saved
        settings.save()


class RatCog(commands.GroupCog):
    setup_hook: Callable[[], Coroutine[Any, Any, None]] | None = None
    """Method called after initialization. As this may be called
    during RatBot.setup_hook, its warnings apply."""
    on_ready_hook: None | Callable[[], Coroutine[Any, Any, None]] = None
    """Method added to bot loop after on_ready. Prefer setup_hook where possible,
    as using this this will allow the cog to continue regardless instead of erroring out."""

    def __init__(self, bot: RatBot) -> None:
        self.bot = bot
        if self.on_ready_hook:
            # create task to add to loop later after bot is ready
            async def func(hook=self.on_ready_hook):
                await bot.wait_until_ready()
                print(self.bot.owner_id)
                try:
                    await hook()
                except Exception as err:
                    message = _format_exception(err)
                    logging.critical(message)
                    await channels.wait_until_loaded()
                    await channels.errors.send(
                        f"An exception was raised in `on_ready_hook` in the following cog: `{type(self)}`\n"
                        + codeblock(message, lang="py")
                    )

            bot.loop.create_task(func())

    @classmethod
    async def basic_setup(cls, bot: RatBot):
        cog = cls(bot)
        await bot.add_cog(cog)
        # since setup_hook is a coroutine, it must be handled here and not in __init__
        if cog.setup_hook:
            await cog.setup_hook()


RatCtx = commands.Context[RatBot]
