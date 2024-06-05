import random
import re

from disnake import Message

from lib import Cog


class Reactions(Cog):
    @Cog.listener()
    async def on_parseable_message(self, message: Message, _: str) -> None:
        if not message.content:
            return

        for reaction in self.settings.reaction_emojis:
            if (
                re.search(reaction.trigger, message.content)
                and random.random() < reaction.chance
            ):
                await message.add_reaction(random.choice(reaction.reactions))
