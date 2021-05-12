import discord.ext.commands as commands
from discord import Color, Embed, Guild


class GuildUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def embed_constructor(self, color: Color, guild: Guild, action: str) -> Embed:
        print(self.bot.user)
        embed = Embed(
            title=f"{action} guild: \"{guild.name}\"",
            description=f"id: `{guild.id}`\n"
                        f"members: {guild.member_count}\n",
            color=color
        ).set_thumbnail(url=guild.icon_url
                        ).set_footer(text=f"total guilds: {len(self.bot.guilds)}")
        return embed

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = await self.embed_constructor(Color.green(), guild, "Joined")
        await self.bot.config.channels.guilds.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        embed = await self.embed_constructor(Color.red(), guild, "Left")
        await self.bot.config.channels.guilds.send(embed=embed)


def setup(bot):
    bot.add_cog(GuildUpdate(bot))
