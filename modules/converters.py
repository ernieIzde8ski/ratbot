from discord.ext import commands
from json import loads
from json.decoder import JSONDecodeError
import re


class FlagConverter(commands.Converter):
    """Convert flags to a dictionary"""

    async def convert(self, ctx: commands.Context, arguments: str) -> dict:
        if not arguments.startswith("--"):
            raise commands.BadArgument("Arguments must begin with --")
        dict_ = {}
        arguments = arguments.replace(";", " ")
        arguments = re.split(r"\s*--\s*", arguments)[1:]
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
                    value = loads(value)
                except JSONDecodeError:
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
                return float(re.sub(r"\s*%", "", "".join(argument.split()))) / 100
            except ValueError:
                raise commands.BadArgument(
                    "Argument must be of the format 0.P or P%"
                )


class Coordinates(commands.Converter):
    """Convert an input to degrees of latitude/longitude"""
    @staticmethod
    def strip(string: str) -> str:
        return "".join(string.split())

    async def convert(self, ctx: commands.Context, argument: str) -> list[int]:
        arguments = re.split(r",\s*|\s+(?=\d)", argument)
        arguments = [self.strip(argument)
                     for argument in arguments if argument]

        if arguments.__len__() > 2:
            raise commands.TooManyArguments(
                "More than two coordinate arguments were passed.")
        elif arguments.__len__() < 2:
            raise commands.BadArgument(
                "Less than two coordinate arguments were passed.")

        arguments = [re.split(r"(?i)(?<=\d)(?:Degrees|Deg(\.)?|°)?(?!\d)", argument)
                     for argument in arguments]
        arguments = [[i for i in index if i] for index in arguments]

        coords = [None, None]
        for index, argument in enumerate(arguments):
            len = argument.__len__()
            if not (1 <= len <= 2):
                raise commands.BadArgument(
                    "More or less than two coordinate arguments were passed")

            if len == 1:
                try:
                    coords[index] = float(argument[0])
                except ValueError:
                    raise commands.BadArgument(
                        "Invalid coordinate arguments passed")
            elif len == 2:
                try:
                    coord_name = argument[1][0].lower()

                    if coord_name == "n":
                        coords[0] = float(argument[0])
                    elif coord_name == "e":
                        coords[1] = float(argument[0])
                    elif coord_name == "w":
                        coords[1] = -float(argument[0])
                    elif coord_name == "s":
                        coords[0] = -float(argument[0])
                except (ValueError, KeyError):
                    raise commands.BadArgument(
                        "Invalid coordinate arguments passed")
        if coords[0] is None or coords[1] is None:
            raise commands.BadArgument(
                "Either latitude or longitude parameter not present")

        if abs(coords[0]) > 90:
            raise commands.BadArgument(
                f"Latitude cannot exceed 90 degrees (given latitude: {coords[0]}).")
        elif abs(coords[1]) > 180:
            raise commands.BadArgument(
                f"Longitude cannot exceed 180 degrees (given longitude: {coords[1]}).")

        return coords


class StrictBool(commands.Converter):
    """Convert a string to bool iff it equals True or False"""
    async def convert(self, ctx: commands.Context, argument: str):
        value = {"true": True, "false": False}.get(argument.lower())
        if value is not None:
            return value
        else:
            raise commands.BadBoolArgument(
                "Could not convert argument to bool")


initial_list_pattern = re.compile(r"(?<!\\),\s*")
secondary_list_pattern = re.compile(r"\s+")


class EasyList(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        arguments = re.split(initial_list_pattern, argument)
        if arguments == [argument]:
            arguments = re.split(secondary_list_pattern, argument)
        return [cleaned_argument for argument in arguments if (cleaned_argument := argument.strip())]
