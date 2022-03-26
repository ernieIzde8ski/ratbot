from pathlib import Path

import discord
from utils import RatCog

_color_outgoing = discord.Color.orange()
_color_incoming = discord.Color.dark_blue()


class DirectMessages(RatCog):
    """Handles DMs both to and from the bot."""

    message: discord.Message | None = None
    """The latest direct message in the bot."""
    downloads: Path = Path("./downloads").absolute()
    if not downloads.exists():
        downloads.mkdir()

    def embed_constructor(self, message: discord.Message) -> discord.Embed:
        bot_is_author = self.bot.user == message.author

        title = str(message.channel)
        color = _color_outgoing if bot_is_author else _color_incoming

        urls = "\n".join(att.url for att in message.attachments[:5])
        max_len = 1900 - len(urls)
        desc = message.content[:max_len] + (message.content[max_len:] and " […]")

        atts = len(message.attachments)
        footer = f"{message.created_at.isoformat(sep=' ', timespec='seconds')} " + (
            f"• Providing links for up to {min(atts, 5)} of {atts} attributes" if atts else ""
        )

        embed = discord.Embed(title=title, description=desc, color=color)
        embed.set_footer(text=footer) # type: ignore
        if urls:
            embed.set_image(url=message.attachments[0].url).add_field(name="Attachments", value=urls, inline=True)
        return embed

    async def direct_message(self, incoming: discord.Message):
        self.message = incoming
        embed = self.embed_constructor(incoming)
        await self.bot.status_channels.DM.send(embed=embed)

    async def downloader(self, attachments: list[discord.Attachment]) -> list[Path]:
        if sum(attachment.size for attachment in attachments) > 6_000_000:
            raise ValueError("Total filesize too large")

        resp = []
        for attachment in attachments:
            path: Path = self.downloads / attachment.filename
            async with self.bot.session.get(attachment.url) as bytes:
                path.write_bytes(await bytes.read())
            resp.append(path)
        return resp

    async def deleter(self, paths: list[Path]):
        for path in paths:
            path.unlink()

    async def channel_message(self, outgoing: discord.Message):
        if outgoing.content == "--DIE":
            await outgoing.reply("No longer replying to the current DM")
            self.message = None
        if outgoing.author.bot or self.message is None: # type: ignore
            return
        # Caps at 7 minutes - the same duration between Discord sending distinct messages
        time_since = outgoing.created_at - self.message.created_at
        if time_since.total_seconds() > 420:
            self.message = None
            return

        try:
            paths = await self.downloader(outgoing.attachments)
        except ValueError as err:
            return await outgoing.reply(f"{err.__class__.__name__}: {err}")

        files = [discord.File(p) for p in paths]
        await self.message.channel.send(f"[{str(outgoing.author)}] {outgoing.content}", files=files)
        await outgoing.delete()
        await self.deleter(paths)

    @RatCog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id in self.bot.blocking:  # type: ignore
            return None
        if not message.guild:
            return await self.direct_message(message)
        if message.channel == self.bot.status_channels.DM:
            return await self.channel_message(message)


setup = DirectMessages.basic_setup
