from discord.ext import commands
from json import loads
from json.decoder import JSONDecodeError

class FlagConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str) -> dict:
        """Converter largely following a discord.py model Lol"""
        # Initialize dict, arguments values
        dict_ = {}
        arguments = argument.split()
        if not arguments:
            raise commands.BadArgument("No arguments exist")

        for argument in iter(arguments):
            if not argument.startswith(("–", "--")):
                raise commands.BadArgument("Argument must begin with -- or –")
            
            # split argument if a value is specified with = or :
            argument = argument.replace("=", ":").split(":")
            if not argument[0]:
                raise commands.BadArgument("Argument value must exist")

            # raise an error if more than one value is passed, or set the value to True if no value is passed
            length = argument.__len__()
            if length > 2:
                raise commands.BadArgument("Argument cannot have more than one value")
            elif length == 1:
                argument.append(True)

            # try and convert the value to another type like int or something
            try:
                argument[1] = loads(argument[1].lower())
            except (JSONDecodeError, AttributeError):
                pass
            
            # replace underscores with spaces in string arguments
            if isinstance(argument[1], str):
                argument[1] = argument[1].replace("_", " ")

            # clean up argument name
            argument[0] = argument[0].removeprefix("--").removeprefix("–").lower()

            # add flag to dictionary
            dict_[argument[0].lower()] = argument[1]
        return dict_
