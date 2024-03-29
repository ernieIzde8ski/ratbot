from discord import Color, Embed, Guild
from discord.ext import commands
from utils import FlagConverter, RatCog


class Guilds(RatCog):
    """Guild status logging"""

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        embed = Embed(
            title=f"Joined guild: {guild}",
            description=f"Members: {guild.member_count}\nID: {guild.id}",
            color=Color.dark_green(),
        ).set_thumbnail(url=guild.icon.url if guild.icon else None)

        await self.bot.status_channels.Guilds.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        embed = Embed(
            title=f"Left guild: {guild}", description=f"ID: {guild.id}", color=Color.dark_red()
        ).set_thumbnail(url=guild.icon.url if guild.icon else None)
        await self.bot.status_channels.Guilds.send(embed=embed)

    @commands.command()
    async def guilds(self, ctx: commands.Context, *, sort: FlagConverter = {}):
        """
        Return guild list
        Usage:
            guilds
            guilds --reverse --order ('member_count' | 'alphabetical')
        """
        order = (sort.get("order") or "alphabetical").lower()
        reverse = bool(sort.get("reverse"))

        if order == "alphabetical":
            guilds = sorted(self.bot.guilds, key=lambda guild: guild.name.lower(), reverse=reverse)
            guilds = map(lambda guild: f"{guild}", guilds)
        elif order == "member_count":
            guilds = sorted(self.bot.guilds, key=lambda guild: guild.member_count or -1, reverse=reverse)
            guilds = map(lambda guild: f"{guild} ({guild.member_count} members)", guilds)
        else:
            raise commands.BadArgument("Invalid sort option")
        await ctx.send("\n".join(guilds))


setup = Guilds.basic_setup
