import re
from aiohttp import ClientSession
from bs4 import BeautifulSoup

url = "https://www.metal-archives.com/band/random"
regex = r"(\n|.+:)"


async def get_bands(loops: int) -> list[list[str, list[str]]]:
    """Get random bands & statistics"""
    band_list = []
    for i in range(loops):
        async with ClientSession() as session:
            async with session.get(url) as resp:
                result = BeautifulSoup(await resp.text(), "html.parser")
                band_name = result.find_all("h1", class_="band_name")[0].text

                stats1 = result.find_all("dl", class_="float_left")[0].text
                stats1 = [i for i in re.split(regex, stats1) if i.split()]
                stats1 = [v for k, v in enumerate(stats1) if k % 2 == 1]

                stats2 = result.find_all("dl", class_="float_right")[0].text
                stats2 = [i for i in re.split(regex, stats2) if i.split()]
                stats2 = [v for k, v in enumerate(stats2) if k % 2 == 1]

                stats = stats1 + stats2
                band_list.append([band_name, stats])
    return band_list


async def format(integer: int = 5):
    """Format random bands"""
    max_band_spaces = 0
    max_genre_spaces = 0
    bands = await get_bands(integer)

    for band in bands:
        len = band[0].__len__() + 2
        if len > max_band_spaces:
            max_band_spaces = len

        len = band[1][4].__len__() + 2
        if len > max_genre_spaces:
            max_genre_spaces = len

    resp = ""
    for band in bands:
        len1 = max_band_spaces - band[0].__len__()
        len2 = max_genre_spaces - band[1][4].__len__()

        resp += band[0] + (" " * len1)
        resp += f"|  Genre(s): {band[1][4]}" + (" " * len2)
        resp += f"|  Region: {band[1][0]}\n"
    return resp
