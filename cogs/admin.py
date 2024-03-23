from disnake.ext import commands

from lib.bot import Bot, Cog, Interaction


class Admin(Cog):
    @commands.slash_command()
    @commands.is_owner()
    async def die(self, inter: Interaction) -> None:
        try:
            await inter.send("Okie dokie", ephemeral=self.settings.hide_mod_commands)
            await self.logs.status.send("im DYING " + self.settings.emoji_offline)
        finally:
            exit(0)


def setup(bot: Bot) -> None:
    bot.add_cog(Admin(bot))
