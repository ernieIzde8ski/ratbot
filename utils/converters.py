from contextlib import suppress
import typing
from discord.ext import commands
from json import loads
from json.decoder import JSONDecodeError
import re


class FlagConverter(commands.Converter):
    """Convert flags to a dictionary"""

    async def convert(self, ctx: commands.Context, arguments: str) -> dict[str, typing.Any]:
        if not arguments.startswith("--"):
            raise commands.BadArgument("Arguments must begin with --")
        resp = {}
        arguments = arguments.replace(";", " ")
        argument_list = re.split(r"\s*--\s*", arguments)[1:]
        for argument in argument_list:
            if not argument:
                raise commands.BadArgument("Argument key must exist")

            value = argument.split()
            key = value.pop(0)

            if not value:
                value = True
            else:
                value = " ".join([i.replace("__", " ") for i in value])
                try:
                    value = loads(value)
                except JSONDecodeError:
                    with suppress(JSONDecodeError):
                        value = loads(value.lower())
            resp[key] = value

        return resp


class Percentage(commands.Converter):
    """Convert a number or string to a percentage if possible"""

    async def convert(self, ctx: commands.Context, argument: str) -> float:
        try:
            return float(argument)
        except ValueError:
            try:
                return float(re.sub(r"\s*%", "", "".join(argument.split()))) / 100
            except ValueError as err:
                raise commands.BadArgument("Argument must be of the format 0.P or P%") from err


class Coordinates(commands.Converter):
    """Convert an input to degrees of latitude/longitude"""

    @staticmethod
    def strip(string: str) -> str:
        return "".join(string.split())

    @staticmethod
    def assert_float(num: typing.Union[float, typing.Literal[None]]) -> float:
        if num is None:
            raise commands.BadArgument("Latitude or longitude not present")
        return num

    async def convert(self, ctx: commands.Context, argument: str) -> list[float]:
        arguments = re.split(r",\s*|\s+(?=\d)", argument)
        arguments = [self.strip(argument) for argument in arguments if argument]

        if arguments.__len__() > 2:
            raise commands.TooManyArguments("More than two coordinate arguments were passed.")
        elif arguments.__len__() < 2:
            raise commands.BadArgument("Less than two coordinate arguments were passed.")

        arguments = [re.split(r"(?i)(?<=\d)(?:Degrees|Deg(\.)?|°)?(?!\d)", argument) for argument in arguments]
        arguments = [[i for i in index if i] for index in arguments]

        coords: list[typing.Union[float, typing.Literal[None]]] = [None, None]
        for i, arg in enumerate(arguments):
            len = arg.__len__()
            if not (1 <= len <= 2):
                raise commands.BadArgument("More or less than two coordinate arguments were passed")

            if len == 1:
                try:
                    coords[i] = float(arg[0])
                except ValueError as e:
                    raise commands.BadArgument("Invalid coordinate arguments passed") from e
            elif len == 2:
                try:
                    coord_name = arg[1][0].lower()

                    if coord_name == "n":
                        coords[0] = float(arg[0])
                    elif coord_name == "e":
                        coords[1] = float(arg[0])
                    elif coord_name == "w":
                        coords[1] = -float(arg[0])
                    elif coord_name == "s":
                        coords[0] = -float(arg[0])
                except (ValueError, KeyError) as e:
                    raise commands.BadArgument("Invalid coordinate arguments passed") from e
        resp = [self.assert_float(coord) for coord in coords]

        if abs(resp[0]) > 90:
            raise commands.BadArgument(f"Latitude cannot exceed 90 degrees (given latitude: {resp[0]}).")
        elif abs(resp[1]) > 180:
            raise commands.BadArgument(f"Longitude cannot exceed 180 degrees (given longitude: {resp[1]}).")

        return resp


class StrictBool(commands.Converter):
    """Convert a string to bool iff it equals True or False"""

    async def convert(self, ctx: commands.Context, argument: str) -> bool:
        value = {"true": True, "false": False}.get(argument.lower())
        if value is not None:
            return value
        else:
            raise commands.BadBoolArgument("Could not convert argument to bool")


initial_list_pattern = re.compile(r"(?<!\\),\s*")
secondary_list_pattern = re.compile(r"\s+")


class EasyList(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str) -> list[str]:
        arguments = re.split(initial_list_pattern, argument)
        if arguments == [argument]:
            arguments = re.split(secondary_list_pattern, argument)
        return [cleaned_argument for argument in arguments if (cleaned_argument := argument.strip())]
