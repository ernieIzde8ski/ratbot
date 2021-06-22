from modules.weather import valid_kwargs, valid_kwarg_types, get_weather
from modules.converters import FlagConverter
from modules.json import safe_load, safe_dump
from typing import Optional, Union
from discord.ext import commands
from discord import Embed


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = safe_load("data/weather_users.json", {})

    @commands.Cog.listener()
    async def on_weather_users_update(self, new_obj):
        safe_dump("data/weather_users.json", new_obj)

    @staticmethod
    async def embed_constructor(weather_data: dict, color) -> Embed:
        main = f"Current: {weather_data['main']['temp']}°\n" \
               f"Feels like: {weather_data['main']['feels_like']}°\n" \
               f"Minimum: {weather_data['main']['temp_min']}°; " \
               f"Maximum: {weather_data['main']['temp_max']}°"
        footer = f"Weather: {weather_data['weather'][0]['description'].title()} | " \
                 f"Pressure: {weather_data['main']['pressure']} hPa | " \
                 f"Humidity: {weather_data['main']['humidity']}%"

        if weather_data["units"].lower() == "metric":
            main = main.replace("°", "°C")
        elif weather_data["units"].lower() == "imperial":
            main = main.replace("°", "°F")
        else:
            main = main.replace("°", "°K")

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
        Gets the weather for a given location
        Accepts either a city as the first parameter, the same flag parameters
        as the set subcommand, or defaults to the set parameter
        Examples:
            r;w south bend
            r;weather Warsaw, IN, US
            r;weather --city_id:4174757 --units:imperial
            r;weather --latitude:0 --longitude:0 --language:pl
            r;weather --zip_code:00-413 --country_code:pl --units:standard
        """
        user_data = self.data.get(str(ctx.author.id))
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

    @weather.command()
    async def set(self, ctx, *, location: Optional[FlagConverter] = {}):
        """
        Saves a default location
        The easiest usage is r;w set --city_name:city_name --units:metric [...]

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
            r;weather set --city_name:Warsaw
            r;w set --city_name=warsaw  --state_code=in --country_code=us --units=imperial
            r;w set --zip_code:00-413 --country_code:pl --units:standard --language:es
            r;w set --latitude=0 --longitude=0 --units=imperial
        """
        if not location:
            return await ctx.send("Please see the help command for proper usage")
        for key in location.keys():
            if key not in valid_kwargs:
                return await ctx.send(f"Error: key {key} is not a valid weather setting")
            elif not isinstance(location[key], valid_kwarg_types[key]):
                return await ctx.send(f"Error: invalid type '{type(location[key]).__name__}' for key {key}")
            if isinstance(location[key], str):
                location[key] = location[key].title().replace("_", " ")
        else:
            set = "Reset" if self.data.get(str(ctx.author.id)) else "Set"
            self.data[str(ctx.author.id)] = location
            self.bot.dispatch("weather_users_update", self.data)
            await ctx.send(f"{set} information, test the weather command to check")


def setup(bot):
    bot.add_cog(Weather(bot))
