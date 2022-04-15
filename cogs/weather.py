import asyncio
import random
import typing
from datetime import datetime, tzinfo
from functools import cache

import discord
from discord.ext import commands
from owmpy.current import StandardUnits
from owmpy.utils import convert_temp
from pytz import BaseTzInfo, timezone
from utils import Coordinates, MaybeUser, RatBot, RatCog, WUser, wowmpy
from utils.functions import safe_load

DescriptionFormat = """
Temperature (Real): {temp}{temp_unit}
Temperature (Felt): {felt}{temp_unit}
{hum}% Humidity with {vis} Visibility
""".strip()

# TODO: Just move the openweathermap module into here hopefully


class WeatherError(commands.CommandError):
    pass


class WeatherNotificationError(WeatherError):
    pass


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
        value: typing.Union[Coordinates, discord.Guild, timezone, str, None],
    ):
        """
        Set location, guild, timezone, or unit data

        Usage:
            weather set 4, 13 # set latitude, longitude
            w s 0413-Theta    # set guild
            w s imperial      # set units
            w s toggle        # toggle daily weather notifications
        """
        if victim and not await self.bot.is_owner(ctx.author):
            raise commands.NotOwner("Only bot owners may specify a victim")
        target: int = (victim or ctx.author).id  # type: ignore
        if value is None:
            return await ctx.send(self.users.all[target])

        if target not in self.users.all:
            self.users.all[target].guild_id = getattr(ctx.guild, "id", None) or self.bot.config.primary_guild

        user = self.users.all[target]

        if isinstance(value, discord.Guild):
            user.guild_id = value.id
            await ctx.send(f"Set guild_id to `{user.guild_id}`.")
        elif isinstance(value, BaseTzInfo):
            user.tz = f"{value}"
            await ctx.send(f"Set tz to `{user.tz}`.")
        elif isinstance(value, list):
            user.coords = wowmpy.WUserCoords(lat=value[0], lon=value[1])
            await ctx.send(f"Set coords to `{user.coords}`.")
        elif isinstance(value, str):
            try:
                units = self.rwth.validate_units(value).api_name
                user.units = units  # type: ignore
                await ctx.send(f"Set units to `{user.units}`")
            except ValueError as err:
                raise ValueError(
                    f"{err}\n"
                    + ", if you are trying to set a timezone, see here for a valid list: "
                    + "<https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568>"
                ) from err
        else:
            raise commands.CommandError(f"Couldn't do shit: class '{value.__class__}'")

        self.rwth.save()

    @weather.command(aliases=["e"])
    @commands.is_owner()
    async def expose(self, ctx: commands.Context, *, target: MaybeUser = None):
        """Displays weather data from a given user. Defaults to self."""
        id: int = (target or ctx.author).id  # type: ignore

        if id not in self.users.all:
            raise ValueError(f"No data for user with id {id}")
        await ctx.send(self.users.all[id])

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


class WeatherNotifications(RatCog):
    """The daily dispatch of weather notifications."""

    def __init__(self, bot: RatBot):
        super().__init__(bot)
        self.rwth = bot.weather
        self.users = bot.weather.data.users
        self.resps = bot.weather.data.resps
        self.russian: list[str] = safe_load("data/russian_bible.json")

    @staticmethod
    @cache
    def tz(__tz: str) -> tzinfo:
        return timezone(__tz)

    def today(self, __tz: str, fmt: str = r"%Y-%m-%d") -> str:
        return datetime.now(tz=self.tz(__tz)).strftime(fmt)

    def temp_eval(self, temp: int | float) -> str:
        return next((_eval for num, _eval in self.resps.temp_reactions if num > temp), self.resps.final_reaction)

    @staticmethod
    def _prepare_resp(__input: typing.Iterable[str | typing.Iterable[str]]) -> str:
        __input = (i if isinstance(i, str) else " ".join(i) for i in __input)
        return "\n\n".join(__input)

    def message_constructor(self, user: WUser, stats: wowmpy.CurrentWeatherStatus) -> str:
        greeting = random.choice(self.rwth.data.resps.greetings)
        alias = random.choice(user.aliases)

        temp = round(stats.main.temp, 1)
        felt = round(stats.main.feels_like, 1)
        _eval = self.temp_eval(convert_temp(temp, __from=stats.units, __to=StandardUnits.METRIC))

        russian = random.choices(self.russian, k=random.randint(2, 5))
        russian[0] = f"**{russian[0]}"
        russian[-1] = f"{russian[-1]}**"

        resp = [
            "__**Здавстуй**__",
            f"{greeting.format(alias)} hope you have Exciting Day. (Just kidding your Stupid)",
            [
                f"It is currently {temp} degrees {stats.units.temp[1]}",
                f"(and it Feels like {felt}{stats.units.temp[0]})," if felt != temp else ",",
                f"with cloudiness of {stats.clouds.all}%.",
                f"In Fact, the Weather is {stats.weather[0].description.title()}, with a humidity",
                f"of {stats.main.humidity}% and windspeeds at {stats.wind.speed} {stats.units.speed[1]}.",
                _eval,
            ],
            russian,
        ]

        return self._prepare_resp(resp)

    async def additional_messaging(self, channel: discord.TextChannel):
        prompt = await channel.send("do you want a Song ?")

        def check(__m: discord.Message):
            return (
                __m.channel == prompt.channel and __m.author != prompt.author and __m.content[:1].lower() in {"y", "n"}
            )

        try:
            message: discord.Message = await self.bot.wait_for("message", timeout=300.0, check=check)
        except asyncio.TimeoutError:
            return await channel.send(self.resps.music_ignored)

        await asyncio.sleep(1 + random.random())
        if message.content[:1] in {"y", "Y"}:
            await channel.send(random.choice(self.resps.music_approved))
            await channel.send("https://youtu.be/" + random.choice(list(self.songs)))
        else:
            await channel.send(random.choice(self.resps.music_rejected))

    @RatCog.listener()
    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        if (
            after.id not in self.users.active  # type: ignore
            or (user := self.users.all[after.id]).guild_id != after.guild.id  # type: ignore
            or before.raw_status != "offline"
            or after.raw_status in ("idle", "offline")
            or user.last_sent == (today := self.today(user.tz))
        ):
            return

        if user.coords is None:
            user.last_sent = today
            raise WeatherNotificationError(
                f"User {after} has notifications enabled, but does not have coordinates set up!"
            )

        stats = await self.rwth.fetch_user(after.id)  # type: ignore
        content = self.message_constructor(user=user, stats=stats)

        try:
            message: discord.Message = await after.send(content)
        except discord.Forbidden as err:
            await self.bot.status_channels.BM.send(
                f"{err.__class__.__name__}: {err}\n"
                f"User {after} most likely has me blocked ; removing from active weather notification list"
            )
            return self.users.active.remove(after.id)  # type: ignore

        user.last_sent = today
        if random.random() < self.rwth.data.music_chance:
            await self.additional_messaging(channel=message.channel)
        self.rwth.save()


async def setup(bot: RatBot):
    bot.reset_weather()
    await bot.add_cog(WeatherCommands(bot))
    await bot.add_cog(WeatherNotifications(bot))
    bot.weather.save()
