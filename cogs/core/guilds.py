from typing import Optional, Union

import discord.ext.commands as commands
from discord import Color, Embed, Guild


class GuildUpdate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sorts = {
            "alphabetical": ["alphabetical", "alphabetic", "a-z", "az"],
            "length": ["lengths", "length", "len"],
            "total_members": ["total_members", "member_list", "members"]
        }

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

    def sort_guilds(self, guilds: list, sort_method: str = "alphabetical", sort_order: Optional[bool] = False) -> \
            Union[list, bool]:
        sort_method = sort_method.lower().replace(" ", "_")
        if sort_method in self.sorts['alphabetical']:
            guilds.sort(key=lambda g: g.name.lower(), reverse=sort_order)
        elif sort_method in self.sorts['length']:
            guilds.sort(key=lambda g: len(g.name), reverse=sort_order)
        elif sort_method in self.sorts['total_members']:
            guilds.sort(key=lambda g: g.member_count, reverse=sort_order)
        else:
            return False
        return guilds

    @commands.command(aliases=["guilds", "list_servers", "servers"])
    @commands.is_owner()
    async def list_guilds(self, ctx, sort_order: Optional[bool] = False, *, sort_method: Optional[str] = "az"):
        """Print list of guilds the bot is a member of
        Parameters:
            sort_order: Reverse the sort order
            sort_method: Self-explanatory
        Valid sort_methods:
            "alphabetical": ["alphabetical", "alphabetic", "a-z", "az"],
            "length": ["lengths", "length", "len"],
            "total_members": ["total_members", "member_list", "members"]"""
        guilds = self.bot.guilds
        if sort_method:
            guilds = self.sort_guilds(guilds, sort_method, sort_order)
            if not guilds: return await ctx.send("This is not a valid sort method")
        guilds = "\n".join([f"{guild} `({guild.member_count})`" for guild in guilds])

        embed = Embed(description=guilds).set_footer(text=f"total guilds: {len(self.bot.guilds)}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(GuildUpdate(bot))
