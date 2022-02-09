from typing import Optional, Union

from discord import Color, Embed, User
from discord.ext import commands
from utils.classes import RatBot
from utils.converters import Coordinates, FlagConverter
from utils.functions import safe_dump
from utils.weather_retrieval import valid_kwarg_types, valid_kwargs


class Weather(commands.Cog):
    def __init__(self, bot: RatBot):
        self.bot = bot
        bot.data.load_weather_configs()

    async def _update(self):
        safe_dump("data/weather_locations.json", self.bot.data.users)

    @staticmethod
    async def embed_constructor(weather_data: dict, color: Color) -> Embed:
        main = (
            f"Current: {weather_data['main']['temp']}°\n"
            f"Feels like: {weather_data['main']['feels_like']}°\n"
            f"Minimum: {weather_data['main']['temp_min']}°; "
            f"Maximum: {weather_data['main']['temp_max']}°"
        )
        footer = (
            f"Weather: {weather_data['weather'][0]['description'].title()} | "
            f"Pressure: {weather_data['main']['pressure']} hPa | "
            f"Humidity: {weather_data['main']['humidity']}%"
        )

        main = main.replace("°", "°" + weather_data["units"]["temp"][:1])

        if weather_data["sys"].get("country"):
            country = ", " + weather_data["sys"]["country"] + "."
        else:
            country = "."

        if weather_data["name"]:
            title = f"Weather for {weather_data['name']}" + country
        else:
            coords = [round(weather_data["coord"]["lat"], 2), round(weather_data["coord"]["lon"], 2)]
            title = f"Weather at {coords[0]}° lat, {coords[1]}° long"

        return Embed(title=title, description=main, color=color).set_footer(text=footer)

    @staticmethod
    def verify_location_data(weather_data: dict) -> None:
        """Raises an error if the argument is invalid"""
        if weather_data == {}:
            raise commands.MissingRequiredArgument("location is a required argument that is missing.")
        for key, value in weather_data.items():
            if key not in valid_kwargs:
                raise commands.BadArgument(f"key {key} is not valid")
            elif not isinstance(value, valid_kwarg_types[key]):
                raise commands.BadArgument(f"invalid type '{value.__class__.__name__}' for key {key}")
            if isinstance(value, str):
                weather_data[key] = weather_data[key].title()

    async def assess_weather(self, ctx: commands.Context, *, location: dict[str, str]) -> None:
        # Retrieve weather data.
        weather_data = await self.bot.weather.get_weather(**location)

        # Utilize weather data.
        if weather_data.get("error"):
            raise commands.CommandError(weather_data["error"])
        embed = await self.embed_constructor(weather_data=weather_data, color=ctx.me.color)
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, aliases=["w"])
    async def weather(self, ctx: commands.Context, *, location: Optional[Union[FlagConverter, str]] = None):
        """Returns the weather for a given location

        Accepts either a city as the first parameter, the same flag parameters
        as the set subcommand, or defaults to the set parameter
        """
        user_data = self.bot.data.users["_"].get(str(ctx.author.id))

        # Raise an error if neither user data is set nor location data is provided.
        if not location and not user_data:
            raise commands.BadArgument(
                f"No weather information provided. " f"Try: \n```\n{prefix}{ctx.invoked_with} <city>\n```"
            )

        # Handle a given input.
        if location is None:
            # If no given input, use the set location data.
            location = user_data["location"]
        elif isinstance(location, dict):
            self.verify_location_data(location)
        elif isinstance(location, str):
            location = {"city_name": location}

        await self.assess_weather(ctx, location=location)

    @weather.group(invoke_without_command=True, aliases=["s"])
    async def set(self, ctx: commands.Context, *, location: FlagConverter = {}):
        """Sets a default location

        The easiest usage is r;w set --city_name:city_name --units:metric [...]
        Note that this WILL override your current settings. Alternatively, subcommands exist.

        Valid locations:
            - city_id
                - city.list.json available at http://bulk.openweathermap.org/sample/
            - latitude, longitude
            - zip_code(, country_code)
            - city_name(, state_code(, country_code))
        Optional options:
            - units: can be any of [standard, metric, imperial], defaults to metric
            - lang: language code
                - see https://openweathermap.org/current#multi
        examples:
            r;w set --city_name Warsaw --state_code IN --country_code US --units Imperial
            r;w set --zip_code 00-413 --country_code PL --units Standard --lang ES
            r;w set --lat 0 --lon 0 --units Imperial
        """
        self.verify_location_data(location)
        id = str(ctx.author.id)
        set = "Reset" if self.bot.data.users.get(id) else "Set"
        self.bot.data.users[id] = location
        await self._update()
        await ctx.send(f"{set} weather information.")

    @set.command(aliases=["a"])
    @commands.is_owner()
    async def admin(self, ctx: commands.Context, victim: Union[int, User], *, location: FlagConverter = None):
        """Check a user's weather, or if given, replace their settings."""
        if location is None:
            user_data = self.bot.data.users["_"].get(str(victim if isinstance(victim, int) else victim.id))
            if user_data is None:
                raise commands.BadArgument("No weather information has been provided.")
            self.verify_location_data(user_data["location"])
            await self.assess_weather(ctx, location=user_data["location"])
        else:
            key = str(victim if isinstance(victim, int) else victim.id)
            self.verify_location_data(location)
            set = "Reset" if self.bot.data.users.get(key) else "Set"
            if not self.bot.data.users["_"].get(key):
                self.bot.data.users["_"][key] = {"location": {}}
            self.bot.data.users["_"][key]["location"] = location
            await self._update()
            await ctx.send(f"{set} `{victim}`'s information")

    @set.command()
    async def city(self, ctx: commands.Context, *, city_name_or_id: Union[int, str]):
        """Sets a city location"""
        # Determine whether its an ID or the name of a city.
        if isinstance(city_name_or_id, int):
            data = {"city_id": city_name_or_id}
        elif isinstance(city_name_or_id, str):
            data = {"city_name": city_name_or_id, "state_code": None, "country_code": None}

        # Use the user ID as a dictionary key.
        key = str(ctx.author.id)
        if self.bot.data.users.get(key) is None:
            self.bot.data.users["_"][key] = {"location": {}}

        #  Update user data.
        self.bot.data.users["_"][key]["location"].update(data)
        safe_dump("data/weather_locations.json", self.bot.data.users)

        # Return a message.
        item = list(data.items())[0]
        await ctx.send(f"Updated `{item[0]}` to `{item[1]}`.")

    @set.command(aliases=["lat-lon", "c"])
    async def coords(self, ctx: commands.Context, *, coords: Coordinates):
        """Sets latitude/longitude coordinates"""
        user = str(ctx.author.id)
        if not self.bot.data.users["_"].get(user):
            self.bot.data.users["_"][user] = {"location": {}}
        self.bot.data.users["_"][user]["location"]["lat"] = coords[0]
        self.bot.data.users["_"][user]["location"]["lon"] = coords[1]
        await self._update()
        await ctx.send(f"Set `latitude`, `longitude` to {coords[0]}, {coords[1]}")


def setup(bot: RatBot):
    bot.add_cog(Weather(bot))
