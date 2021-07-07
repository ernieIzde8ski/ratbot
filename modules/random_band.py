import re
from aiohttp import ClientSession
from bs4 import BeautifulSoup
from textwrap import shorten


url = "https://www.metal-archives.com/band/random"
regex = r"(\n|.+:)"


async def get_bands(loops: int) -> list[dict]:
    """Get random bands & statistics"""
    band_list = []
    async with ClientSession() as session:
        for i in range(loops):
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
                stats = {
                    "origin": [stats[0], stats[1]], "status": stats[2],
                    "formed": stats[3], "genre": stats[4], "lyrics": stats[5],
                    "label": stats[6], "name": band_name
                }
                band_list.append(stats)
    return band_list


async def format(integer: int = 5):
    """Format random bands"""
    max_band_spaces = 7
    max_genre_spaces = 11
    bands = await get_bands(integer)

    for band in bands:
        band["name"] = shorten(band["name"], 30)
        len = band["name"].__len__() + 2
        if len > max_band_spaces:
            max_band_spaces = len

        band["genre"] = shorten(band["genre"], 30)
        len = band["genre"].__len__() + 2
        if len > max_genre_spaces:
            max_genre_spaces = len

    len1 = (max_band_spaces - 6) * " "
    len2 = (max_genre_spaces - 10) * " "
    resp = f"Band: {len1}" \
           f"|  " \
           f"Genre(s): {len2}" \
           f"|  " \
           f"Region:\n"

    for band in bands:
        len1 = max_band_spaces - band["name"].__len__()
        len2 = max_genre_spaces - band["genre"].__len__()

        resp += band["name"] + (" " * len1)
        resp += f"|  {band['genre']}" + (" " * len2)
        resp += f"|  {band['origin'][0]}\n"
    return resp
