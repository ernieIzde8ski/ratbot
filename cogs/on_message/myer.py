import json
from random import choice

import discord.ext.commands as commands
from discord import AllowedMentions, Forbidden


class Myer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("cogs/on_message/myer.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def response(self):
        """Generate response"""
        # actually generate response
        if str(self.data['responses_given']) in list(self.data['responses']):
            response = self.data['responses'][str(self.data['responses_given'])]
        else:
            response = choice(self.data['responses']['generic'])
        # return response
        return response

    async def respond(self, msg):
        if not msg.guild: return
        if msg.guild.id != 488475203303768065: return
        # check if the guild is 0413-Theta

        # check for twitter links from myer
        if "https://twitter.com" in msg.content and msg.author.id == self.data['myer']:
            # Punishment.
            try:
                await msg.delete()
            except Forbidden:
                return await msg.channel.send("Hit me, nail me, make me God !!!!!!!!!!!")
            await msg.channel.send(
                f"{msg.author.mention} {self.response()}", allowed_mentions=AllowedMentions(users=True)
            )
            with open("cogs/on_message/myer.json", "w", encoding="utf-8") as f:
                self.data["responses_given"] += 1
                json.dump(self.data, f)

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.respond(message)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        await self.respond(after)


def setup(bot):
    bot.add_cog(Myer(bot))
