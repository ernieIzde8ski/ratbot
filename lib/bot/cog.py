import asyncio
import inspect
import logging
from asyncio import sleep
from functools import cached_property

from disnake import AppInfo, ClientUser
from disnake.ext.commands import Cog as BaseCog

from lib.bot.log_channels import LogChannels

from ..settings import Settings
from .bot import Bot


class Cog(BaseCog):
    bot: Bot
    """The Bot instance this cog belongs to."""
    settings: Settings
    """Alias for bot.settings"""

    # the following items are cached properties so that they don't need
    # to use any post_init_hook magic
    @cached_property
    def logs(self) -> LogChannels:
        """Alias for bot.logs"""
        return self.bot.logs

    @cached_property
    def user(self) -> ClientUser:
        """Alias for bot.user"""
        return self.bot.user

    @cached_property
    def app_info(self) -> AppInfo:
        return self.bot.app_info

    async def post_init_hook(self) -> None:
        """
        Override this hook for any cog that needs to do some additional setup once ready.
        """

    async def __post_init_hook__(self):
        """Runner for the post init hook."""
        while self.bot.supplements_loaded is False:
            await sleep(0)
        await self.post_init_hook()

    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot
        self.settings = bot.settings

        # checks if the hook was overridden
        if type(self).post_init_hook != Cog.post_init_hook:
            asyncio.create_task(self.__post_init_hook__())

    @classmethod
    def __init_subclass__(cls, /, include_setup: bool = True) -> None:
        """Defines the setup function for most subclassing cogs."""
        if include_setup is False:
            return

        ext = inspect.getmodule(cls)
        if ext is None:
            return logging.warn(f"Could not find module for cog: '{cls.__name__}'")
        ext.__dict__["setup"] = lambda bot: bot.add_cog(cls(bot))
