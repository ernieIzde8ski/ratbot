from discord.ext import commands
from utils.classes import RatBot


class WeatherEvents(commands.Cog):
    def __init__(self, bot: RatBot) -> None:
        self.bot = bot


def setup(bot: RatBot):
    bot.reset_weather()
    bot.add_cog(WeatherEvents(bot))
