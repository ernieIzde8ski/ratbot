from discord.ext import commands
from json import loads
from json.decoder import JSONDecodeError


class FlagConverter(commands.Converter):
    async def convert(self, ctx: commands.Context, argument: str):
        """Converter largely following a discord.py model Lol"""
        dict_ = {}
        arguments = argument.replace(" ", "").split(",")
        if not arguments:
            raise commands.BadArgument("No arguments exist")

        for argument in arguments:
            if not argument.startswith(("–", "--")):
                raise commands.BadArgument("Argument must begin with -- or –")
            argument = argument.replace("=", ":").split(":")
            if not argument[0]:
                raise commands.BadArgument("Argument value must exist")
            length = argument.__len__()
            if length > 2:
                raise commands.BadArgument("Argument cannot have more than one value")
            elif length == 1:
                argument.push(True)

            try:
                argument[1] = loads(argument[1].lower())
            except JSONDecodeError:
                pass
            finally:
                dict_[argument[0].lower()] = argument[1]
        return dict_
