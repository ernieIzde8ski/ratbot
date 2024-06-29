import re
from contextlib import suppress

from disnake import AllowedMentions, Forbidden, HTTPException, Message
from thefuzz import fuzz

from lib import Cog

from .commands import COMMANDS

pattern = re.compile(r"^git\s+([^\s]+)")

GIT_HELP: str = """
```
'git help -a' and 'git help -g' list available subcommands and some
concept guides. See 'git help <command>' or 'git help <concept>'
to read about a specific subcommand or concept.
See 'git help git' for an overview of the system.
```
"""

NO_MENTIONS: AllowedMentions = AllowedMentions.none()


class Git(Cog):
    @Cog.listener()
    async def on_parseable_message(self, message: Message, _: str) -> None:
        match = re.match(pattern, message.content)
        if match is None:
            return

        input_cmd = match[1]
        if input_cmd[0] == input_cmd[-1] and input_cmd[0] in ("'", '"'):
            input_cmd = input_cmd[1:-1]

        reply: str

        if input_cmd in ["--help", "help"]:
            reply = GIT_HELP
        elif input_cmd in COMMANDS:
            reply = "lmao no fuck you"
        else:
            reply = f"git: '{input_cmd}' is not a git command. See 'git --help'."

            similarities = [(fuzz.ratio(input_cmd.lower(), cmd), cmd) for cmd in COMMANDS]
            similarities = sorted((s for s in similarities if s[0] > 66), reverse=True)
            if similarities and similarities[0][0] > 90:
                similar_words = [similarities[0][1]]
            else:
                similar_words = sorted(s[1] for s in similarities[:3])

            match len(similar_words):
                case 0:
                    pass
                case 1:
                    reply += "\n        ".join(
                        ("\n\nThe most similar command is", similar_words[0])
                    )
                case _:
                    reply += "\n        ".join(
                        ("\n\nThe most similar commands are", *similar_words)
                    )

            reply = f"```text\n{reply}\n```"

        with suppress(Forbidden, HTTPException):
            await message.reply(reply, allowed_mentions=NO_MENTIONS)
