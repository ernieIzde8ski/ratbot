import typing

import discord
from discord.ext import commands
from utils import Coordinates, MaybeUser, RatBot, RatCog, wowmpy

DescriptionFormat = """
Temperature (Real): {temp}{temp_unit}
Temperature (Felt): {felt}{temp_unit}
{hum}% Humidity with {vis} Visibility
""".strip()

# TODO: Just move the openweathermap module into here hopefully


class WeatherCommands(RatCog):
    """Commands to get the weather and set your location."""

    def __init__(self, bot: RatBot):
        super().__init__(bot)
        self.rwth = bot.weather
        self.users = bot.weather.data.users

    @staticmethod
    def message_embed(status: wowmpy.CurrentWeatherStatus) -> discord.Embed:
        """Generates an embed for weather"""
        description = DescriptionFormat.format(
            temp=status.main.temp,
            felt=status.main.feels_like,
            temp_unit=status.units.temp[0],
            hum=status.main.humidity,
            vis=status.visibility,
        )
        footer = (
            f"Condition: {status.weather[0].description.title()}",
            f"Pressure: {status.main.pressure} {status.units.pressure}",
            f"Cloudiness: {status.clouds.all}%",
        )
        embed = discord.Embed(
            title=f"The Present Weather in {status.name or (status.coord.lat, status.coord.lon)}",
            description=description,
        )
        return embed.set_footer(text=" | ".join(footer))  # type: ignore

    @commands.group(invoke_without_command=True, aliases=["w"])
    async def weather(self, ctx: commands.Context, *, coords: Coordinates):  # type: ignore
        status = await self.rwth.fetch(coords)
        embed = self.message_embed(status)
        await ctx.send(embed=embed)

    @weather.command(aliases=["s"])
    async def set(
        self,
        ctx: commands.Context,
        victim: MaybeUser = None,
        *,
        value: typing.Union[Coordinates, discord.Guild, str, None],
    ):
        """Set location, guild, or unit data"""
        if victim and not await self.bot.is_owner(ctx.author):
            raise commands.NotOwner("Only bot owners may specify a victim")
        target: int = (victim or ctx.author).id  # type: ignore
        if value is None:
            raise ValueError

        if target not in self.users.all:
            self.users.all[target].guild_id = getattr(ctx.guild, "id", None) or self.bot.config.primary_guild

        user = self.users.all[target]

        if isinstance(value, discord.Guild):
            user.guild_id = value.id
            await ctx.send(f"Set guild_id to `{user.guild_id}`.")
        elif isinstance(value, list):
            user.coords = wowmpy.WUserCoords(lat=value[0], lon=value[1])
            await ctx.send(f"Set coords to `{user.coords}`.")
        elif isinstance(value, str):
            units = self.rwth.validate_units(value).api_name
            user.units = units  # type: ignore
            await ctx.send(f"Set units to `{user.units}`")
        else:
            raise commands.CommandError(f"Couldn't do shit: class '{value.__class__}'")
        
        self.rwth.save()

    @weather.command(aliases=["toggle"])
    async def toggle_active(self, ctx: commands.Context, *, user: MaybeUser = None):
        if user and not await self.bot.is_owner(ctx.author):
            raise commands.NotOwner("Only bot owners may specify user")
        id: int = (user or ctx.author).id  # type: ignore
        if id in self.users.active:
            self.users.active.remove(id)
            await ctx.send(f"Disabled weather notifications for user `{id=}`")
        else:
            self.users.active.add(id)
            await ctx.send(f"Enabled weather notifications for user `{id=}`")


def setup(bot: RatBot):
    bot.reset_weather()
    bot.add_cog(WeatherCommands(bot))
    bot.weather.save()
