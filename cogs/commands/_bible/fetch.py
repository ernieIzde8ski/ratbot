from os import error
from textwrap import fill
from typing import Dict, TypedDict

from aiohttp import ClientSession
from attr import dataclass


class BibleError(Exception):
    """Raised on sacrilegious defilement"""
    pass


class TranslationError(Exception):
    def __init__(self, ver: str | None = None) -> None:
        self.ver = ver
        super().__init__(
            "Translation not found" if not ver else f"Translation '{ver}' not found")

    # def __str__(self) -> str:
    #     return self.msg if not self.ver else f"Translation {self.ver} not found"


@dataclass
class RawVerse(TypedDict):
    book_id: str
    book_name: str
    chapter: int
    verse: int
    text: str


@dataclass
class RawBibleResponse(TypedDict):
    reference: str
    verses: list[RawVerse]
    text: str
    translation_id: str
    translation_name: str
    translation_note: str


@dataclass
class CleanBibleResponse(TypedDict):
    reference: str
    verses: list[RawVerse]
    text: str
    translation_id: str
    translation_name: str


class Translation:
    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name


class ProcessedBibleResponse:
    ref: str
    verses: list[str]
    tr: Translation
    text: str

    def __init__(self, ref: str, verses: list[str], text: str, tr_id: str, tr_name: str) -> None:
        self.ref = ref
        self.verses = verses
        self.text = text
        self.tr = Translation(tr_id, tr_name)


# BibleParams = Mapping[str, str]


class PassageRetrieval:
    def __init__(self, session: ClientSession = None) -> None:
        self.session = session or ClientSession()

    @staticmethod
    def process(cleaned_resp: CleanBibleResponse, width: int = 70):
        return ProcessedBibleResponse(
            ref=cleaned_resp["reference"],
            verses=[verse["text"] for verse in cleaned_resp["verses"]],
            text=fill(cleaned_resp["text"], width),
            tr_id=cleaned_resp["translation_id"], tr_name=cleaned_resp["translation_name"]
        )

    @staticmethod
    def __clean(resp: RawBibleResponse) -> CleanBibleResponse:
        del resp["translation_note"]
        for index in range(len(resp["verses"])):
            resp["verses"][index]["text"] = resp["verses"][index]["text"].strip().replace(
                "\n", "")
        resp["text"] = resp["text"].replace("\n", " ").strip()
        return resp

    async def retrieve(self, ref: str, *, translation: str = "KJV", verse_numbers: bool = False) -> CleanBibleResponse:
        Params = {}
        if translation:
            Params["translation"] = translation
        if verse_numbers is not None:
            Params["verse_numbers"] = str(verse_numbers)

        async with self.session.get(f"https://bible-api.com/{ref}", **{"params": Params}) as result:
            result: RawBibleResponse | Dict["error", str] | str = (await result.json())

            if result.get("error"):
                raise BibleError(result[error])
            elif isinstance(result, str):
                raise BibleError(result)
            elif not isinstance(result, Dict):
                raise Exception("Something has gone horribly wrong")

        return self.__clean(result)

    async def procget(self, ref: str, translation: str = None, verse_numbers: bool = None, width: int = 70) -> ProcessedBibleResponse:
        """Shorthand for `await self.get(); await self.process();`."""
        resp = await self.retrieve(ref, verse_numbers=verse_numbers, translation=translation)
        return self.process(resp, width)
