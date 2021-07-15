from discord import Embed, User
from discord.ext import commands
from typing import Optional, Union

from modules._json import safe_load, safe_dump
from modules.converters import FlagConverter
from modules.weather import valid_kwargs, valid_kwarg_types, get_weather


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.userlocs = safe_load("data/weather_locations.json", {})

    async def _update(self):
        safe_dump("data/weather_locations.json", self.bot.userlocs)

    @staticmethod
    async def embed_constructor(weather_data: dict, color) -> Embed:
        main = f"Current: {weather_data['main']['temp']}°\n" \
               f"Feels like: {weather_data['main']['feels_like']}°\n" \
               f"Minimum: {weather_data['main']['temp_min']}°; " \
               f"Maximum: {weather_data['main']['temp_max']}°"
        footer = f"Weather: {weather_data['weather'][0]['description'].title()} | " \
                 f"Pressure: {weather_data['main']['pressure']} hPa | " \
                 f"Humidity: {weather_data['main']['humidity']}%"

        main = main.replace("°", "°" + weather_data["units"]["temp"][:1])

        if weather_data['sys'].get("country"):
            country = ", " + weather_data['sys']['country'] + "."
        else:
            country = "."

        if weather_data['name']:
            title = f"Weather for {weather_data['name']}" + country
        else:
            coords = [round(weather_data["coord"]["lat"], 2),
                      round(weather_data["coord"]["lon"], 2)]
            title = f"Weather at {coords[0]}° lat, {coords[1]}° long"

        return Embed(
            title=title,
            description=main,
            color=color
        ).set_footer(text=footer)

    @commands.group(invoke_without_command=True, aliases=["w"])
    async def weather(self, ctx, *, location: Optional[Union[FlagConverter, str]]):
        """
        Returns the weather for a given location
        Accepts either a city as the first parameter, the same flag parameters
        as the set subcommand, or defaults to the set parameter
        """
        user_data = self.bot.userlocs.get(str(ctx.author.id))
        if not location and not user_data:
            prefix = ctx.prefix.replace('`', '\`')
            return await ctx.send("Invalid usage; "
                                  f"`{prefix}{ctx.invoked_with} <city>`")
        elif not location:
            weather_data = await get_weather(self.bot.config["weather"], **user_data)
        else:
            if isinstance(location, str):
                weather_data = await get_weather(self.bot.config["weather"], city_name=location)
            elif isinstance(location, dict):
                weather_data = await get_weather(self.bot.config["weather"], **location)
        if weather_data.get("error"):
            return await ctx.send(f"Error: {weather_data['error']}")
        await ctx.send(embed=await self.embed_constructor(weather_data=weather_data, color=ctx.me.color))

    @weather.group(invoke_without_command=True, aliases=["s"])
    async def set(self, ctx, *, location: Optional[FlagConverter] = {}):
        """
        Sets a default location
        The easiest usage is r;w set --city_name:city_name --units:metric [...]
        Subcommands also exist if you don't feel like doing that

        Valid locations:
            - city_id
                - city.list.json.gz available at http://bulk.openweathermap.org/sample/
            - latitude, longitude
            - zip_code(, country_code)
            - city_name(, state_code(, country_code))
        Optional options:
            - units: can be any of [standard, metric, imperial], defaults to metric
            - language: language code
                - ie --language:pl will render in polish
                - see https://openweathermap.org/current#multi

        examples:
            r;w set --city_name Warsaw  --state_code IN --country_code US --units Imperial
            r;w set --zip_code 00-413 --country_code PL --units Standard --language ES
            r;w set --latitude 0 --longitude 0 --units Imperial
        """
        if not location:
            return await ctx.send("Please see the help command for proper usage")
        for key, value in location.items():
            if key not in valid_kwargs:
                raise commands.BadArgument(f"key {key} is not a valid weather setting")
            elif not isinstance(value, valid_kwarg_types[key]):
                raise commands.BadArgument(f"invalid type '{value.__class__.__name__}' for key {key}")
            if isinstance(value, str):
                location[key] = location[key].title().replace("_", " ")
        else:
            id = str(ctx.author.id)
            set = "Reset" if self.bot.userlocs.get(id) else "Set"
            self.bot.userlocs[id] = location
            await self._update()
            await ctx.send(f"{set} information")

    @set.command()
    @commands.is_owner()
    async def admin(self, ctx, victim: Union[User, int], *, location: FlagConverter = {}):
        """Force set a user's location settings"""
        if isinstance(victim, User):
            victim = victim.id
        victim = str(victim)

        for key, value in location.items():
            if key not in valid_kwargs:
                raise commands.BadArgument(f"key {key} is not a valid weather setting")
            elif not isinstance(value, valid_kwarg_types[key]):
                raise commands.BadArgument(f"invalid type '{value.__class__.__name__}' for key {key}")
            if isinstance(value, str):
                location[key] = location[key].title().replace("_", " ")
        else:
            set = "Reset" if self.bot.userlocs.get(victim) else "Set"
            self.bot.userlocs[victim] = location
            await self._update()
            await ctx.send(f"{set} `{victim}`'s information")

    @set.command()
    async def city(self, ctx, *, city_name_or_id: Union[int, str]):
        """Sets a city location"""
        user = str(ctx.author.id)
        if not self.bot.userlocs.get(user):
            self.bot.userlocs[user] = {}
        if isinstance(city_name_or_id, int):
            type_ = "city_id"
            self.bot.userlocs[user][type_] = city_name_or_id
        elif isinstance(city_name_or_id, str):
            city_name_or_id = city_name_or_id.replace(", ", ",").split(",")
            list_ = list(city_name_or_id)
            type_ = "city_name"
            self.bot.userlocs[user][type_] = list_.pop(0)
            if list_:
                type_ = [type_, "state_code"]
                self.bot.userlocs[user][type_[1]] = list_.pop(0)
            if list_:
                type_ += ["country_code"]
                self.bot.userlocs[user][type_[1]] = list_.pop(0)
            if list_:
                return await ctx.send("Too many codes passed")
        await self._update()
        await ctx.send(f"Set `{type_}` to {city_name_or_id}")

    @set.command(aliases=["lat-long"])
    async def coords(self, ctx, lat: Union[int, float], long: Union[int, float]):
        """
        Sets latitude/longitude coordinates
        The only accepted two inputs are integers or floats; this means no funny
        inputs like 'r;w set coords 50°S, 50°E'. This would rather be
        represented as `r;w set coords -50 50'.
        """
        user = str(ctx.author.id)
        if not self.bot.userlocs.get(user):
            self.bot.userlocs[user] = {}
        if abs(lat) > 90:
            return await ctx.send(f"Error: Latitude cannot exceed 90 degrees")
        elif abs(long) > 180:
            return await ctx.send(f"Error: Longitude cannot exceed 180 degrees")
        else:
            self.bot.userlocs[user]["latitude"] = lat
            self.bot.userlocs[user]["longitude"] = long
        await self._update()
        await ctx.send(f"Set `latitude`, `longitude` to {lat}, {long}")


def setup(bot):
    bot.add_cog(Weather(bot))
