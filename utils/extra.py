from functools import cache
from typing import TYPE_CHECKING
from discord import Interaction
if TYPE_CHECKING:
    from .models import RatBot

def codeblock(string: str, lang: str | None = None):
    return f"```{lang or ''}\n{string.rstrip()}\n```"

@cache
def is_owner():
    def pred(interaction: Interaction):
        if TYPE_CHECKING:
            assert isinstance(interaction.client, RatBot)
        return interaction.client.is_owner(interaction.user)
    return pred