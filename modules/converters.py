from typing import Union
from discord.ext import commands
from json.decoder import JSONDecodeError
from json import loads
from re import split, sub


class FlagConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, arguments: str) -> dict:
        if not arguments.startswith("--"):
            raise commands.BadArgument("Arguments must begin with --")
        dict_ = {}
        arguments = arguments.replace(";", " ")
        arguments = split(r"\s+--", arguments[2:])
        for argument in arguments:
            if not argument:
                raise commands.BadArgument("Argument key must exist")

            value = argument.split()
            key = value.pop(0)

            if not value:
                value = True
            else:
                value = " ".join([i.replace("__", " ") for i in value])
                try:
                    value = loads(value.lower())
                except JSONDecodeError:
                    pass

            dict_[key] = value

        return dict_


class Percentage(commands.Converter):
    """Convert a number or string to a percentage if possible"""
    async def convert(self, ctx: commands.Context, argument: str):
        try:
            return float(argument)
        except ValueError:
            try:
                return float(sub(r"\s*%", "", argument)) / 100
            except ValueError:
                raise commands.BadArgument(
                    "Argument must be of the format 0.25 or 25%")
