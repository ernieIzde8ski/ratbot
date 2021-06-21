from aiohttp import ClientSession


def get_weather_url(apikey: str, **kwargs) -> str:
    """
    Gets the url for an api call to openweathermap
    Necessary kwargs (any of these work, evaluated in this order):
        - city_id: int
            - city.list.json.gz downloadable at http://bulk.openweathermap.org/sample/
        - latitude: int, longitude: int
        - zip_code, country_code
        - zip_code
        - city_name, state_code, country_code
        - city_name, state_code
        - city_name
    Optional kwargs:
        - units: str (default: metric)
        - language: str
            - is a language code, not the full name; see https://openweathermap.org/current#multi for codes
    """
    if kwargs.get("city_id"):
        url = f"https://api.openweathermap.org/data/2.5/weather?id={kwargs['city_id']}"
    elif kwargs.get("latitude") and kwargs.get("longitude"):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={kwargs['latitude']}&lon={kwargs['longitude']}"
    elif kwargs.get("zip_code") and kwargs.get("country_code"):
        url = f"https://api.openweathermap.org/data/2.5/weather?zip={kwargs['zip_code']},{kwargs['country_code']}"
    elif kwargs.get("zip_code"):
        url = f"https://api.openweathermap.org/data/2.5/weather?zip={kwargs['zip_code']}"
    elif kwargs.get("city_name") and kwargs.get("state_code") and kwargs.get("country_code"):
        url = f"api.openweathermap.org/data/2.5/weather?q={kwargs['city_name']},{kwargs['state_code']},{kwargs['country_code']}"
    elif kwargs.get("city_name") and kwargs.get("state_code"):
        url = f"api.openweathermap.org/data/2.5/weather?q={kwargs['city_name']},{kwargs['state_code']}"
    elif kwargs.get("city_name"):
        url = f"api.openweathermap.org/data/2.5/weather?q={kwargs['city_name']}"
    else:
        raise KeyError("No valid kwargs given")

    if kwargs.get("units"):
        url += f"&units={kwargs['units']}"
    else:
        url += "&units=metric"

    if kwargs.get("language"):
        url += f"&lang={kwargs['language']}"

    return url + f"&appid={apikey}"


async def get_weather(apikey, **kwargs):
    """Returns a dict object with weather information
    takes the same parameters as get_weather_url"""
    try:
        url = get_weather_url(apikey, **kwargs)
    except KeyError:
        return {"error": "invalid kwargs\n "}

    async with ClientSession() as session:
        async with session.get(url) as resp:
            resp = await resp.json()
            if resp.get("message"):
                return {"error": resp["message"]}
            else:
                return resp
