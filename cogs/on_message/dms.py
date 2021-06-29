from discord.ext import commands
from discord import Embed, Color


class DMs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild or message.author.id in self.bot._check.blocked:
            return

        if message.author.id != self.bot.user.id:
            title = f"Direct Message from {message.channel.recipient}"
            color = Color.dark_blue()
        elif message.author.id == self.bot.user.id:
            title = f"Direct Message to {message.channel.recipient}"
            color = Color.orange()

        embed = await self.embed_constructor(message, title, color)
        await self.bot.c.DMs.send(embed=embed)
        self.bot.dispatch("private_message", message)

    @staticmethod
    async def embed_constructor(message, title: str, color: Color) -> Embed:
        urls = [a.url for a in message.attachments]
        maximum_length = 1900 - len(" ".join(urls))
        if len(message.content) > maximum_length:
            message.content = message.content[:maximum_length] + " […]"
        description = f"{message.content}"
        if urls:
            description += "\n\n\n**Attachment URLs: \n**"
            description += "\n".join(urls)
        embed = Embed(title=title, description=description, color=color)
        if message.attachments:
            embed.set_image(
                url=message.attachments[0].url
            ).set_footer(
                text=f"{len(message.attachments)} attachment(s)"
            )
        return embed


def setup(bot):
    bot.add_cog(DMs(bot))
