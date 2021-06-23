from aiohttp import ClientSession

valid_kwarg_types = {
    "city_id": int, "latitude": (int, float), "longitude": (int, float), "zip_code": (str, int), 
    "country_code": str, "state_code": str, "city_name": str, "units": str, "language": str
}
valid_kwargs = list(valid_kwarg_types.keys())


def get_weather_url(apikey: str, **kwargs) -> str:
    """
    Gets the url for an api call to openweathermap
    Necessary kwargs (any of these work, evaluated in this order):
        - city_id: int
            - city.list.json.gz available at http://bulk.openweathermap.org/sample/
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
    url = "https://api.openweathermap.org/data/2.5/weather"
    if kwargs.get("city_id"):
        url += f"?id={kwargs['city_id']}"
    elif (kwargs.get("latitude") != None) and (kwargs.get("longitude") != None):
        url += f"?lat={kwargs['latitude']}&lon={kwargs['longitude']}"
    elif kwargs.get("zip_code") and kwargs.get("country_code"):
        url += f"?zip={kwargs['zip_code']},{kwargs['country_code']}"
    elif kwargs.get("zip_code"):
        url += f"?zip={kwargs['zip_code']}"
    elif kwargs.get("city_name") and kwargs.get("state_code") and kwargs.get("country_code"):
        url += f"?q={kwargs['city_name']},{kwargs['state_code']},{kwargs['country_code']}"
    elif kwargs.get("city_name") and kwargs.get("state_code"):
        url += f"?q={kwargs['city_name']},{kwargs['state_code']}"
    elif kwargs.get("city_name"):
        url += f"?q={kwargs['city_name']}"
    else:
        raise KeyError("No valid kwargs given")

    if kwargs.get("units"):
        url += f"&units={kwargs['units']}"
    else:
        url += "&units=metric"

    if kwargs.get("language"):
        url += f"&lang={kwargs['language']}"

    return url + f"&appid={apikey}"


async def get_weather(apikey: str, **kwargs) -> dict:
    """Returns a dict object with weather information
    takes the same parameters as get_weather_url"""
    try:
        url = get_weather_url(apikey, **kwargs)
    except KeyError:
        return {"error": "invalid kwargs\nPlease verify your location data"}

    async with ClientSession() as session:
        async with session.get(url) as resp:
            resp = await resp.json()
            if resp.get("message"):
                return {"error": resp["message"]}
            else:
                if kwargs.get("units"):
                    resp["units"] = kwargs["units"]
                else: 
                    resp["units"] = "metric"
                return resp
