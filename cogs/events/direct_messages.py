import logging
import re
from datetime import UTC, datetime, timedelta

from disnake import Color, Embed, File, Message, User
from disnake.abc import Messageable

from lib import Bot, Cog, TemporaryAttachmentHolder

COLOR_SELF = Color.orange()
COLOR_OTHER = Color.green()


class DirectMessages(Cog):
    """Listens for private messages and relays them to a channel."""

    latest_message: Message | None = None
    """Last private message received."""

    delay: timedelta
    """Delay before latest_message is disregarded."""

    def __init__(self, bot: Bot) -> None:
        super().__init__(bot)
        self.delay = timedelta(seconds=self.settings.dm_expiry_delay)

    async def relay_incoming(self, message: Message, /) -> None:
        """Relays "incoming" messages - those in DMs, sent by rat or not."""
        its_not_me = message.author.id != self.bot.user.id
        if message.author.bot and its_not_me:
            return

        color = COLOR_OTHER if its_not_me else COLOR_SELF

        recipient: User | None = message.author if its_not_me else message.channel.recipient  # type: ignore

        embed = Embed(description=message.content, color=color)
        if recipient is not None:
            embed = embed.set_author(
                name=recipient, icon_url=recipient.display_avatar.url
            )
        else:
            embed = embed.set_author(name=message.channel)
        tah = TemporaryAttachmentHolder(self.session, message)
        files: list[File] = []

        if len(message.attachments) == 1 and message.attachments[
            0
        ].filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            embed.set_image(message.attachments[0].url)
        elif message.attachments:
            await tah._open()
            files = tah.as_files()

        try:
            m = await self.logs.dms.send(embed=embed, files=files)
        finally:
            self.latest_message = message
            tah.close()

    __target_pattern = re.compile(
        r"(?:TO:|@)\s*([^\n]+)\n+(.+)", re.MULTILINE | re.DOTALL
    )

    async def relay_outgoing(self, message: Message, /) -> None:
        """Relays "outgoing" messages - those sent in the dedicated `logs.dms` channel."""
        if message.author.bot:
            return

        message_content: str
        target: Messageable  # technically User | DMChannel, but this is hard to write

        # get message content & shit
        match = re.match(self.__target_pattern, message.content)
        if match is not None:
            try:
                user_id = int(match[1])
                target = await self.bot.getch_user(user_id, strict=True)
                message_content = match[2]
            except ValueError as parent_error:
                error = Exception(f"could not parse user id: '{match[1]}'")
                raise error from parent_error
        elif self.latest_message is None:
            return
        elif (datetime.now(UTC) - self.latest_message.created_at) > self.delay:
            self.latest_message = None
            return
        else:
            target = self.latest_message.channel
            message_content = message.content

        async with TemporaryAttachmentHolder(self.session, message) as tah:
            await target.send(message_content, files=tah.as_files())

        await message.delete()

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if message.guild is None:
            try:
                await self.relay_incoming(message)
            except Exception:
                logging.exception("couldn't relay a message")
        elif message.channel == self.logs.dms:
            try:
                await self.relay_outgoing(message)
            except Exception:
                logging.exception("couldn't send a message")
                await message.reply("couldn't send this message, check logs")
