from typing import Union
from discord.ext import commands
from discord import Activity, ActivityType, Game, Status
from modules.converters import FlagConverter


class Stati(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.loop.create_task(self.initialize())

    async def initialize(self) -> None:
        await self.bot.wait_until_ready()
        activity = Activity(
            name=self.bot.config["default_status"].format(
                self.bot.config["prefix"][0]
            ),
            type=ActivityType.watching
        )
        await self.bot.change_presence(activity=activity)

    @staticmethod
    def get_status(status: str):
        status = str(status).lower()
        try:
            return getattr(Status, status)
        except AttributeError:
            return None

    @commands.command()
    @commands.is_owner()
    async def set_presence(self, ctx, *, presence: Union[FlagConverter, str]):
        if isinstance(presence, dict):
            activity = Game(presence.get("activity"))
            status = self.get_status(presence.get("status"))
        else:
            activity = Game(name=presence)
            status = None
        await self.bot.change_presence(activity=activity, status=status)
        await ctx.send(f"Set activity, status to {activity}, {status}")


def setup(bot):
    bot.add_cog(Stati(bot))