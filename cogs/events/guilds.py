from discord import Guild, Embed, Color
from discord.ext import commands

from modules.converters import FlagConverter


class Guilds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        embed = Embed(
            title=f"Joined guild: {guild}",
            description=f"Members: {guild.member_count}\nID: {guild.id}",
            color=Color.dark_green()
        ).set_thumbnail(url=guild.icon_url)
        await self.bot.c.Guilds.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        embed = Embed(
            title=f"Left guild: {guild}",
            description=f"ID: {guild.id}",
            color=Color.dark_red()
        ).set_thumbnail(url=guild.icon_url)
        await self.bot.c.Guilds.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def guilds(self, ctx: commands.Context, *, sort: FlagConverter = {}):
        """
        Return guild list
        Usage:
            r;guilds
            r;guilds --order member_count --reverse
        """
        order = "alphabetical" if not (order := sort.get("order")) else order.lower()
        reverse = bool(sort.get("reverse"))

        if order == "alphabetical":
            guilds = sorted(self.bot.guilds, key=lambda guild: guild.name.lower(), reverse=reverse)
            guilds = map(lambda guild: f"{guild}", guilds)
        elif order == "member_count":
            guilds = sorted(self.bot.guilds, key=lambda guild: guild.member_count, reverse=reverse)
            guilds = map(lambda guild: f"{guild} ({guild.member_count} members)", guilds)
        else:
            raise commands.BadArgument("Invalid sort option")
        await ctx.send("\n".join(guilds))


def setup(bot):
    bot.add_cog(Guilds(bot))
