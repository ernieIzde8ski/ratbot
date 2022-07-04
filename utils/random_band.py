import re
from textwrap import shorten
from typing import Hashable, TypedDict

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from unidecode import unidecode


url = "https://www.metal-archives.com/band/random"
regex = r"(\n|.+:)"


class Band(TypedDict):
    origin: tuple[str, str]
    status: str
    formed: str
    genre: str
    lyrics: str
    label: str
    name: str
    url: str


class BandRetrieval:
    def __init__(self):
        self.session = ClientSession()
        self.iterations = {}

    async def __aenter__(self):
        pass

    async def __aexit__(self, *args):
        await self.session.close()

    async def close(self):
        return await self.__aexit__()

    async def _get_bands(
        self, loops: int, index: Hashable, *, _filter: str = "", max_iterations: int = 50
    ) -> list[Band]:
        """Get random bands & statistics"""
        _filter = _filter.lower()
        bands = []
        for _ in range(loops):
            self.iterations[index] += 1
            try:
                async with self.session.get(url) as resp:
                    result = BeautifulSoup(await resp.text(), "html.parser")
                    band_name = result.find_all("h1", class_="band_name")[0].text

                    stats1 = result.find_all("dl", class_="float_left")[0].text
                    stats1 = [i for i in re.split(regex, stats1) if i.split()]
                    stats1 = [v for k, v in enumerate(stats1) if k % 2 == 1]

                    stats2 = result.find_all("dl", class_="float_right")[0].text
                    stats2 = [i for i in re.split(regex, stats2) if i.split()]
                    stats2 = [v for k, v in enumerate(stats2) if k % 2 == 1]

                    stats = stats1 + stats2
                    band = Band(
                        origin=(stats[0], stats[1]),
                        status=stats[2],
                        formed=stats[3],
                        genre=stats[4],
                        lyrics=stats[5],
                        label=stats[6],
                        name=band_name,
                        url=str(resp.url),
                    )
            except IndexError:
                band = (await self._get_bands(1, index, _filter=_filter, max_iterations=max_iterations))[0]
            if _filter not in band["genre"].lower() and _filter not in band["name"].lower():
                if self.iterations[index] >= max_iterations:
                    continue
                band = await self._get_bands(1, index, _filter=_filter, max_iterations=max_iterations)
                if band == []:
                    continue
                band = band[0]
            bands.append(band)
        return bands

    async def get_bands(
        self, max_bands: int, hash: Hashable, *, _filter: str = "", max_iterations: int = 50
    ) -> list[Band]:
        self.iterations[hash] = 0
        bands = await self._get_bands(max_bands, hash, _filter=_filter, max_iterations=max_iterations)
        del self.iterations[hash]
        return bands

    async def format(
        self, cache_index: str, max_bands: int = 5, sort_method: str = "band", *, _filter: str = ""
    ) -> str:
        """Format random bands"""
        bands = await self.get_bands(max_bands, cache_index, _filter=_filter)

        if bands == []:
            return "Couldn't find a single goddamn band with those parameters. Good job."

        if (sort_method := sort_method.lower()) == "band":
            bands.sort(key=lambda band: unidecode(band["name"].lower()))
        elif sort_method == "genre":
            bands.sort(key=lambda band: unidecode(band["genre"].lower()))
        elif sort_method == "region":
            bands.sort(key=lambda band: unidecode(band["origin"][0].lower()))

        max_band_spaces = 7
        max_genre_spaces = 11
        for band in bands:
            band["name"] = shorten(band["name"], 30)
            len = band["name"].__len__() + 2
            if len > max_band_spaces:
                max_band_spaces = len

            # I abuse the textwrap module by adding a space, which will cause
            # the genre name to be split on slashes. This prevents lines like
            # While Heaven Wept  |  Epic [...]                     |  United States
            # from occurring when genres are separated by slashes. Instead:
            # While Heaven Wept  |  Epic Progressive/Power/[...]   |  United States
            band["genre"] = shorten(band["genre"].replace("/", "/ "), 30, replace_whitespace=False).replace("/ ", "/")
            len = band["genre"].__len__() + 2
            if len > max_genre_spaces:
                max_genre_spaces = len

        len1 = (max_band_spaces - 6) * " "
        len2 = (max_genre_spaces - 10) * " "
        resp = f"Band: {len1}" f"|  " f"Genre(s): {len2}" f"|  " f"Region:\n"

        for band in bands:
            len1 = max_band_spaces - band["name"].__len__()
            len2 = max_genre_spaces - band["genre"].__len__()

            resp += band["name"] + (" " * len1)
            resp += f"|  {band['genre']}" + (" " * len2)
            resp += f"|  {band['origin'][0]}\n"
        return resp
