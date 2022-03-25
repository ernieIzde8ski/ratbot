import typing

import discord


Bible = dict[str, str]
"""A dictionary mapping member ID to translation. Corresponds to bible.json."""

Russian = list[str]
"""A list of bible verses. Corresponds to russian.json."""

MaybeUser = typing.Union[discord.Member, discord.User, None]
"""Equivalent to `typing.Union[discord.Member, discord.User, None]`"""
