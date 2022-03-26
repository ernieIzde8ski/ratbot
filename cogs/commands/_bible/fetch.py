from os import error
from textwrap import fill
from typing import TypedDict

from aiohttp import ClientSession
from attr import dataclass


class BibleError(Exception):
    """Raised on sacrilegious defilement"""

    pass


class TranslationError(Exception):
    def __init__(self, ver: str | None = None) -> None:
        self.ver = ver
        super().__init__(f"Translation '{ver}' not found" if ver else "Translation not found")


@dataclass
class RawVerse(TypedDict):
    book_id: str
    book_name: str
    chapter: int
    verse: int
    text: str


class RawBibleResponse(TypedDict):
    reference: str
    verses: list[RawVerse]
    text: str
    translation_id: str
    translation_name: str
    translation_note: str


class CleanBibleResponse:
    reference: str
    verses: list[RawVerse]
    text: str
    translation_id: str
    translation_name: str

    def __init__(self, raw: RawBibleResponse):
        self.reference = raw["reference"]
        self.translation_id = raw["translation_id"]
        self.translation_name = raw["translation_name"]

        self.text = raw["text"].strip().replace("\n", "")
        self.verses = []
        for verse in raw["verses"]:
            verse["text"] = verse["text"].strip().replace("\n", "")
            self.verses.append(verse)


class Translation:
    def __init__(self, id: str, name: str) -> None:
        self.id = id
        self.name = name


@dataclass
class ProcessedBibleResponse:
    ref: str
    verses: list[str]
    tr: Translation
    text: str


class PassageRetrieval:
    def __init__(self, session: ClientSession | None = None) -> None:
        self.session = session or ClientSession()

    @staticmethod
    def process(clean: CleanBibleResponse, width: int = 70) -> ProcessedBibleResponse:
        return ProcessedBibleResponse(
            ref=clean.reference,
            verses=[verse["text"] for verse in clean.verses],
            text=fill(clean.text, width),
            tr=Translation(clean.translation_id, clean.translation_name),
        )

    async def retrieve(
        self, ref: str, *, translation: str | None = None, verse_numbers: bool | None = False
    ) -> CleanBibleResponse:
        Params = {}
        if translation:
            Params["translation"] = translation
        if verse_numbers is not None:
            Params["verse_numbers"] = str(verse_numbers)

        async with self.session.get(f"https://bible-api.com/{ref}", **{"params": Params}) as resp:
            result: (RawBibleResponse or dict["error", str] or str) = await resp.json()

            if isinstance(result, str):
                raise BibleError(result)
            elif err := result.get("error"):
                if err == "not found":
                    err = "Text not found"
                raise BibleError(err)
            elif not isinstance(result, dict):
                raise BibleError("Something has gone horribly wrong")

        return CleanBibleResponse(result)

    async def procget(
        self, ref: str, translation: str | None = None, verse_numbers: bool | None = None, width: int = 70
    ) -> ProcessedBibleResponse:
        """Shorthand for `await self.get(); await self.process();`."""
        resp = await self.retrieve(ref, verse_numbers=verse_numbers or False, translation=translation)
        return self.process(resp, width)
