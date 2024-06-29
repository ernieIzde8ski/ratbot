from pathlib import Path
from typing import Iterable

from thefuzz import fuzz

cwd = Path(__file__).parent
with open(cwd / "commands.txt") as file:
    _commands = file.read().splitlines()

COMMANDS: set[str] = {cmd.removeprefix("git-") for cmd in _commands if cmd}
"""List of git commands, ripped from man pages."""


def get_similar_commands(comp_str: str, threshold: int = 66) -> Iterable[str]:
    comp_str = comp_str.lower()
    for command in COMMANDS:
        if fuzz.ratio(comp_str, command) > threshold:
            yield comp_str
