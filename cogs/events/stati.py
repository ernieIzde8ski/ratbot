from discord import Activity, ActivityType, Game, Status
from discord.ext import commands
from utils import FlagConverter, RatCog


class Stati(RatCog):
    """Status management"""

    async def _on_ready(self):
        await self.bot.wait_until_ready()
        activity = Activity(name=self.bot.config.status.format(self.bot.config.prefix[0]), type=ActivityType.watching)
        await self.bot.change_presence(activity=activity)

        self.bot.app = await self.bot.application_info()
        self.bot.owner_id = self.bot.app.owner.id

    @staticmethod
    def get_status(status: str):
        return getattr(Status, status.lower(), None)

    @commands.command()
    @commands.is_owner()
    async def set_presence(self, ctx: commands.Context, *, presence: FlagConverter | str):
        """Sets a presence

        Usage:
            set_presence a Fun Video-Game
            set_presence --activity Fun Video-Igri --status idle
        """
        if isinstance(presence, dict):
            activity = Game(presence.get("activity"))
            status = self.get_status(presence.get("status"))
        else:
            activity = Game(name=presence)
            status = None
        await self.bot.change_presence(activity=activity, status=status)
        await ctx.send(f"Set activity, status to {activity}, {status}")


setup = Stati.basic_setup
