import typing

import discord
from discord.ext import commands
from utils._types import MaybeUser
from utils.classes import RatBot, RatCog
from utils.converters import Coordinates
from utils.openweathermap import CurrentWeatherStatus, NamedCoords, RatWeather, WUser

DescriptionFormat = """
Temperature (Real): {temp}{temp_unit}
Temperature (Felt): {felt}{temp_unit}
{hum}% Humidity with {vis} Visibility
""".strip()

rwth: RatWeather
"""An alias of bot.weather so I don't have ridiculous lines like
`if target.id not in self.bot.weather.data.active_users`"""
# TODO: Just move the openweathermap module into here hopefully


class WeatherCommands(RatCog):
    """Commands to get the weather and set your location."""

    @staticmethod
    def message_embed(status: CurrentWeatherStatus) -> discord.Embed:
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
            f"",
        )
        embed = discord.Embed(
            title=f"The Present Weather in {status.name or (status.coord.lat, status.coord.lon)}",
            description=description,
        )
        return embed.set_footer(text=" | ".join(footer))  # type: ignore

    @commands.group(invoke_without_command=True, aliases=["w"])
    async def weather(self, ctx: commands.Context, *, coords: Coordinates):  # type: ignore
        status = await rwth.fetch(coords)
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
        if victim and not await self.bot.is_owner(ctx.author):
            raise commands.NotOwner("Only bot owners may specify a victim")
        target: int = (victim or ctx.author).id  # type: ignore
        if value is None:
            raise ValueError

        if target not in rwth.data.configs:
            target_coords = NamedCoords(lat=0, lon=0)
            target_guild_id: int = getattr(ctx.guild, "id", None) or self.bot.config["primary_guild"]
            rwth.data.configs[target] = WUser(coords=NamedCoords(lat=0, lon=0), guild_id=target_guild_id)
            await ctx.send(
                f"Initialized {target} data at coordinates `{target_coords=}` and guild `{target_guild_id=}`"
            )

        usr = rwth.data.configs[target]

        if isinstance(value, discord.Guild):
            if not ctx.guild:
                raise commands.GuildNotFound("Must be called in a guild!")
            usr.guild_id = ctx.guild.id  # type: ignore
            await ctx.send(f"Set guild_id to `{usr.guild_id}`.")
        elif isinstance(value, list):
            usr.coords = NamedCoords(*value)
            await ctx.send(f"Set coords to `{usr.coords}`.")
        elif isinstance(value, str):
            units = rwth._units(value).api_name
            usr.units = units  # type: ignore
            await ctx.send(f"Set units to `{usr.units}`")
        else:
            raise commands.CommandError(f"Couldn't do shit: class '{value.__class__}'")

        rwth.save()

    @weather.command(aliases=["toggle"])
    async def toggle_active(self, ctx: commands.Context, *, user: MaybeUser = None):
        if user and not await self.bot.is_owner(ctx.author):
            raise commands.NotOwner("Only bot owners may specify user")
        id: int = (user or ctx.author).id  # type: ignore
        if id in rwth.data.active_users:
            rwth.data.active_users.remove(id)
            await ctx.send(f"Disabled weather notifications for user `{id=}`")
        else:
            rwth.data.active_users.add(id)
            await ctx.send(f"Enabled weather notifications for user `{id=}`")


def setup(bot: RatBot):
    bot.reset_weather()
    global rwth
    rwth = bot.weather
    bot.add_cog(WeatherCommands(bot))
    bot.weather.save()
