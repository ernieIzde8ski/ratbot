import asyncio
import logging
from pathlib import Path
from typing import Awaitable, Self

from aiohttp import ClientSession
from disnake import File, Message
from xdg_base_dirs import xdg_cache_home

cache_dir: Path = xdg_cache_home() / "ratbot"

if not cache_dir.exists():
    cache_dir.mkdir()


async def _download(session: ClientSession, path: Path, url: str) -> Path:
    async with session.get(url) as req:
        with open(path, "wb") as file:
            file.write(await req.read())
    return path


class TemporaryAttachmentHolder:
    _paths: list[Path]
    """List to downloaded filepaths."""
    _root: Path
    """Directory containing filepaths."""

    __empty: bool
    """True when the instance has already been consumed or contains no attachments."""
    __message: Message
    """A message containing attachments."""
    __session: ClientSession
    """A ClientSession instance, to make requests with."""

    def __init__(self, session: ClientSession, message: Message) -> None:
        if not message.attachments:
            self.__empty = True
        else:
            self.__empty = False
            self.__message = message
            self.__session = session

    async def _open(self) -> Self:
        if self.__empty:
            return self

        self._root = root = cache_dir / str(self.__message.id)
        root.mkdir()
        logging.debug(f"downloading attachments to {root}")

        coros: list[Awaitable[Path]] = []

        for attachment in self.__message.attachments:
            coro = _download(
                self.__session,
                root / f"{attachment.id}_{attachment.filename}",
                url=attachment.url,
            )
            coros.append(coro)

        self._paths = await asyncio.gather(*coros)
        logging.debug(f"successfully downloaded {len(self._paths)} file(s) to {root}")

        # don't need to hold onto these anymore
        del self.__message
        del self.__session

        return self

    def close(self) -> None:
        if self.__empty:
            return

        for path in self._paths:
            try:
                path.unlink()
            except Exception:
                logging.exception(f"couldn't delete file: {path}")

        self._root.rmdir()

        self.__empty = True

    def as_files(self) -> list[File]:
        if self.__empty:
            return []
        return [File(path) for path in self._paths]

    def __await__(self):
        return self._open().__await__

    def __aenter__(self) -> Awaitable[Self]:
        return self._open()

    async def __aexit__(self, *_args, **_kwargs) -> None:
        return self.close()
