from discord.ext import commands
from re import split
from json import loads
from json.decoder import JSONDecodeError


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
