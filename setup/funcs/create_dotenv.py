from .generics import InputError, register_func
from pathlib import Path

dotenv = Path(".env")


@register_func
def create_dotenv():
    """Creating .env file..."""
    if dotenv.exists():
        cont = input("A .env file already exists. Continue anyways? [y/N]")[:1]
        if cont.lower() != "y":
            return
    with open(dotenv, "a") as file:
        bot_token = input("Provide a Discord bot token: ").strip()
        if not bot_token:
            raise InputError("A token is required.")
        weather_apikey = input("(Optional) Provide an Current Weather Data API key from OpenWeather: ")
        file.write(f"DISCORD_TOKEN={bot_token}")
        file.write(f"WEATHER_TOKEN={weather_apikey}")
