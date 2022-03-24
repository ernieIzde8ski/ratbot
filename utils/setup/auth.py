before_auth = """Setting .env variables. Make sure you have a token from
https://discord.com/developers (required) && an API key from
https://openweathermap.org/api (optional)."""


def ask_for_auth() -> str:
    """Asks for a token & an API key."""
    print(before_auth)
    token = input("Token?   ")
    apikey = input("API key? ")
    if not token:
        raise KeyError("Expected token.")
    resp = f"DISCORD_TOKEN='{token}'\n"
    if not apikey:
        print("Remember to disable the weather cogs!")
    else:
        resp += f"CURRENT_WEATHER_TOKEN='{apikey}'\n"
    return resp
