from discord import Forbidden
from discord.ext import commands

import re
from typing import Optional
from utils.classes import RatBot

from utils.functions import safe_dump
from utils.converters import EasyList, FlagConverter, Percentage


class Settings(commands.Cog):
    def __init__(self, bot: RatBot):
        self.bot = bot

    @commands.command(aliases=["prefix"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_prefix(self, ctx: commands.Context, prefix: Optional[str]):
        """Sets a guild-wide prefix
        --reset can be used to reset the prefix to the default instead"""
        id = str(ctx.guild.id)
        established_prefix = self.bot.pfx.prefixes.get(id)
        # If no prefix argument is passed, display current prefix.
        if prefix is None:
            if established_prefix is not None:
                await ctx.send(f"Your prefix is `{established_prefix}`")
            else:
                raise commands.BadArgument("No prefix is set.")
        # If the prefix argument is an argument to reset, reset the current prefix.
        elif prefix == "--reset":
            if established_prefix is None:
                raise commands.BadArgument("No prefix is set")
            await ctx.send(f"Resetting prefix from `{established_prefix}`")
            await self.bot.pfx.reset(id)
        # If the prefix argument is otherwise present, update the prefix to it.
        else:
            await self.bot.pfx.update(id, prefix)
            await ctx.send(f"Updated prefix to {prefix}.")

    @commands.command(aliases=["tenor_toggle"])
    @commands.has_guild_permissions(manage_guild=True)
    async def toggle_tenors(self, ctx: commands.Context):
        """Toggle Tenor gif deleting"""
        if ctx.guild.id in self.bot.data.tenor_guilds:
            await ctx.send("Disabling tenor slaying in this server")
            self.bot.data.tenor_guilds.remove(ctx.guild.id)
        else:
            await ctx.send("Enabling tenor slaying in this server")
            self.bot.data.tenor_guilds.add(ctx.guild.id)
        safe_dump("data/tenor_guilds.json", list(self.bot.data.tenor_guilds))

    @commands.command(aliases=["toggle_petrosyan", "toggle_pipi"])
    @commands.has_guild_permissions(manage_guild=True)
    async def toggle_petrosian(self, ctx: commands.Context):
        """Toggles the bot DMing individuals the Petrosian copypasta"""
        id = str(ctx.guild.id)
        if id in self.bot.data.pipi_guilds:
            await ctx.send("Reenabling the Petrosian copypasta")
            self.bot.data.pipi_guilds.remove(id)
        else:
            await ctx.send("Disabling the Petrosian copypasta")
            self.bot.data.pipi_guilds.add(id)
        safe_dump("data/pipi.json", list(self.bot.data.pipi_guilds))

    @commands.command(aliases=["toggle_bans"])
    @commands.has_guild_permissions(administrator=True)
    async def toggle_random_bans(self, ctx: commands.Context, *, percent: Percentage | float | None):
        """Toggle the bot randomly banning individuals"""
        id = str(ctx.guild.id)
        if id in self.bot.data.banning_guilds and not percent:
            await ctx.send("Disabling random bans in this guild")
            self.bot.data.banning_guilds.pop(id)
        else:
            if not percent:
                percent = 0.00002
            elif not (0 < percent < 1):
                return await ctx.send("Error: Percentage must be from 0% to 100% (or 0.0 to 1.0)")
            await ctx.send(f"Enabling random bans in this guild with a {percent * 100}% chance")
            self.bot.data.banning_guilds[id] = percent
        safe_dump("data/banning.json", self.bot.data.banning_guilds)

    @commands.command(aliases=["update_trollgex", "troll"])
    @commands.is_owner()
    async def update_troll_regex(self, ctx: commands.Context, *, regex: Optional[str]):
        if regex is None:
            await ctx.send(f"Current regex: `r\"{self.bot.data.trollgex.pattern}\"`")
        else:
            self.bot.data.trollgex = re.compile(regex, re.I)
            safe_dump("data/trollgex.json", regex)
            await ctx.send(f"Set troll regex to {regex}")

    @commands.command(aliases=["append_trolljis", "trolfl"])
    @commands.is_owner()
    async def append_troll_emojis(
            self, ctx: commands.Context, flag: Optional[FlagConverter] = {}, *, trolljis: Optional[EasyList]):
        # TODO: See if works as a tuple instead of custom list constructor. Use `extend`.
        if trolljis is None:
            await ctx.send("Currently enabled troll emojis: {}".format(", ".join(self.bot.data.trolljis)))
        else:
            try:
                for trollji in trolljis:
                    await ctx.message.add_reaction(trollji)
            except (Forbidden):
                pass
            if flag.get("reset"):
                self.bot.data.trolljis = []
            self.bot.data.trolljis += trolljis
            await ctx.send(f"Set troll emojis to: {', '.join(self.bot.data.trolljis)}")


def setup(bot: RatBot):
    bot.add_cog(Settings(bot))
