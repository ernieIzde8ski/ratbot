from discord.ext import commands
from utils.classes import RatBot
import discord

from utils.converters import Coordinates
from utils.openweathermap import NamedCoords, CurrentWeatherStatus

DescriptionFormat = """
Temperature (Real): {temp}{temp_unit}
Temperature (Felt): {felt}{temp_unit}
{hum}% Humidity with {vis} Visibility
""".strip()

class WeatherCommands(commands.Cog):

    def __init__(self, bot: RatBot) -> None:
        self.bot = bot

    def message_embed(self, status: CurrentWeatherStatus) -> discord.Embed:
        description = DescriptionFormat.format(temp=status.main.temp, felt=status.main.feels_like, temp_unit=status.units.temp[0], hum=status.main.humidity, vis=status.visibility)
        footer = f"Condition: {status.weather[0].description.title()}" , f"Pressure: {status.main.pressure} {status.units.pressure}", f"Cloudiness: {status.clouds.all}%", f""
        return discord.Embed(
            title=f"The Present Weather in {status.name or (status.coord.lat, status.coord.lon)}", description=description
        ).set_footer(text=" | ".join(footer))

    @commands.group(invoke_without_command=True, aliases=["w"])
    async def weather(self, ctx: commands.Context, *, coords: Coordinates):  # type: ignore
        
        status = await self.bot.weather.fetch(coords)
        embed = self.message_embed(status)
        await ctx.send(embed=embed)
    
    @weather.command(aliases=["s"])
    async def set(self, ctx: commands.Context, *, coords: Coordinates):
        self.bot.weather.data.configs[ctx.author.id].coords = NamedCoords(*coords)
        self.bot.weather.save()
        await ctx.send(f"Set coords to {coords}!")

def setup(bot: RatBot):
    bot.reset_weather()
    bot.add_cog(WeatherCommands(bot))
    bot.weather.save()
