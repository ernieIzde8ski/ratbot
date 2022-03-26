import contextlib
from typing import Optional

import discord
from discord.ext import commands
from utils import EasyList, FlagConverter, Percentage, RatCog


class Settings(RatCog):
    """Bot-wide settings management"""

    @commands.command(aliases=["prefix", "pfx"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_prefix(self, ctx: commands.Context, prefix: Optional[str] = None):
        """Sets a guild-wide prefix
        --reset can be used to reset the prefix to the default instead"""
        established_prefix = self.bot.prefixes.prefixes.get(ctx.guild.id)
        # If no prefix argument is passed, display current prefix.
        if prefix is None:
            if established_prefix is not None:
                return await ctx.send(f"Your prefix is `{established_prefix}` .")
            else:
                raise commands.BadArgument("No prefix is set.")
        # If the prefix argument is an argument to reset, reset the current prefix.
        elif prefix == "--reset":
            if established_prefix is None:
                raise commands.BadArgument("No prefix is set")
            await ctx.send(f"Resetting prefix from `{established_prefix}`")
            await self.bot.prefixes.reset(ctx.guild.id)
        # If the prefix argument is otherwise present, update the prefix to it.
        else:
            await self.bot.prefixes.update(ctx.guild.id, prefix)
            await ctx.send(f"Updated prefix to `{prefix}` .")
        self.bot.prefixes.save()

    @commands.command(aliases=["toggle_petrosyan", "toggle_pipi"])
    @commands.has_guild_permissions(manage_guild=True)
    async def toggle_petrosian(self, ctx: commands.Context):
        """Toggles the bot DMing individuals the Petrosian copypasta"""
        guild = self.guilds[ctx.guild.id]
        if guild.pipi_enabled:
            await ctx.send("Disabling the Petrosian copypasta")
            guild.pipi_enabled = False
        else:
            await ctx.send("Reenabling the Petrosian copypasta")
            guild.pipi_enabled = True
        self.bot.settings.save()

    @commands.command(aliases=["toggle_bans"])
    @commands.has_guild_permissions(administrator=True)
    async def toggle_random_bans(self, ctx: commands.Context, *, percent: Optional[Percentage | float]):
        """Toggle the bot randomly banning individuals"""
        guild = self.guilds[ctx.guild.id]
        if guild.ban_chance is not None and not percent:
            await ctx.send("Disabling random bans in this guild")
            guild.ban_chance = None
        else:
            if not percent:
                percent = 0.00002
            elif not (0 < percent < 1):
                raise ValueError("Percentage must be from 0% to 100% (0.0 to 1.0)")
            await ctx.send(f"Enabling random bans in this guild with a {percent * 100}% chance")
            guild.ban_chance = percent
        self.bot.settings.save()

    @commands.command(aliases=["append_trolljis", "trolfl"])
    @commands.is_owner()
    async def append_troll_emojis(
        self, ctx: commands.Context, flag: Optional[FlagConverter] = {}, *, trolljis: Optional[EasyList]
    ):
        # TODO: See if works as a tuple instead of custom list constructor. Use `extend`.
        if trolljis is None:
            await ctx.send(f'Currently enabled troll emojis: {", ".join(self.emojis.trolls)}')

        else:
            with contextlib.suppress(discord.Forbidden):
                for trollji in trolljis:
                    await ctx.message.add_reaction(trollji)
            if flag.get("reset"):
                self.emojis.trolls = []
            self.emojis.trolls += trolljis
            self.bot.settings.save()
            await ctx.send(f"Set troll emojis to: {', '.join(self.emojis.trolls)}")


setup = Settings.basic_setup
