import logging

from lib import Bot, Cog


class Admin(Cog):
    async def post_init_hook(self) -> None:
        # this needs to be a post_init_hook because it requires self.logs to be enabled
        logging.info(f"Logged in as {self.user}!")
        await self.logs.status.send("" f"im ALIVE {self.settings.emoji_online}")


def setup(bot: Bot) -> None:
    bot.add_cog(Admin(bot))
