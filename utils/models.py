import logging
import traceback
from typing import Any, Callable, Coroutine

import discord
from discord.ext import commands
from settings import settings


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
        # load enabled extensions
        settings.reduce_enabled_extensions()
        for ext in settings.enabled_extensions:
            try:
                await self.load_extension(ext)
                logging.info(f"Loaded extension: {ext}")
            except Exception as err:
                message = "".join(
                    (
                        f"{err.__class__.__name__}: {err}\n\n",
                        *traceback.format_exception(err),
                    )
                )
                logging.critical(message)

        # make sure settings are saved
        settings.save()


class RatCog(commands.GroupCog):
    setup_hook: Callable[[], Coroutine[Any, Any, None]] | None = None
    """Method called after initialization. As this may be called
    during RatBot.setup_hook, its warnings apply."""
    on_ready_hook: None | Callable[[], Coroutine[Any, Any, None]] = None
    """Method added to bot loop after on_ready. Prefer setup_hook where possible,
    as this will silently fail instead of raising errors."""

    def __init__(self, bot: RatBot) -> None:
        self.bot = bot

    @classmethod
    async def basic_setup(cls, bot: RatBot):
        cog = cls(bot)
        await bot.add_cog(cog)
        if cog.setup_hook:
            await cog.setup_hook()
        if cog.on_ready_hook:

            async def coro(hook=cog.on_ready_hook):
                await bot.wait_until_ready()
                await hook()

            bot.loop.create_task(coro())


RatCtx = commands.Context[RatBot]
