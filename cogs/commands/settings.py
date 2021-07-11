from discord.ext import commands
from typing import Optional

from modules._json import safe_load, safe_dump
from modules.converters import Percentage


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tenor_guilds = set(safe_load("data/tenor_guilds.json", []))
        self.bot.pipi_guilds = set(safe_load("data/pipi.json", []))
        self.bot.banning_guilds = safe_load("data/banning.json", {})

    @commands.command(aliases=["prefix"])
    @commands.has_guild_permissions(manage_guild=True)
    async def set_prefix(self, ctx, prefix: Optional[str]):
        """Sets a guild-wide prefix
        --reset can be used to reset the prefix to the default instead"""
        if not ctx.guild:
            return await ctx.send("You must be in a guild to run this command!")
        id = str(ctx.guild.id)
        if not prefix:
            if self.bot.pfx.prefixes.get(id):
                await ctx.send(f"Your prefix is `{self.bot.pfx.prefixes[id]}`")
            else:
                await ctx.send("Your prefix must have a length!")
        elif prefix == "--reset":
            if self.bot.pfx.prefixes.get(id):
                await ctx.send(f"Resetting prefix from `{self.bot.pfx.prefixes[id]}`")
                await self.bot.pfx.reset(id)
            else:
                await ctx.send("There is no set prefix!")
        else:
            await self.bot.pfx.update(id, prefix)
            prefix = prefix.replace("`", "\`")
            await ctx.send(f"Updated prefix to {prefix}")

    @commands.command(aliases=["tenor_toggle"])
    @commands.has_guild_permissions(manage_guild=True)
    async def toggle_tenors(self, ctx):
        """Toggle Tenor gif deleting"""
        if ctx.guild.id in self.bot.tenor_guilds:
            await ctx.send("Disabling tenor slaying in this server")
            self.bot.tenor_guilds.remove(ctx.guild.id)
        else:
            await ctx.send("Enabling tenor slaying in this server")
            self.bot.tenor_guilds.add(ctx.guild.id)
        safe_dump("data/tenor_guilds.json", list(self.bot.tenor_guilds))

    @commands.command(aliases=["toggle_petrosyan", "toggle_pipi"])
    @commands.has_guild_permissions(manage_guild=True)
    async def toggle_petrosian(self, ctx):
        """Toggles the bot DMing individuals the Petrosian copypasta"""
        id = str(ctx.guild.id)
        if id in self.bot.pipi_guilds:
            await ctx.send("Reenabling the Petrosian copypasta")
            self.bot.pipi_guilds.remove(id)
        else:
            await ctx.send("Disabling the Petrosian copypasta")
            self.bot.pipi_guilds.add(id)
        safe_dump("data/pipi.json", list(self.bot.pipi_guilds))

    @commands.command(aliases=["toggle_bans"])
    @commands.has_guild_permissions(administrator=True)
    async def toggle_random_bans(self, ctx, *, percent: Optional[Percentage]):
        """Toggle the bot randomly banning individuals"""
        id = str(ctx.guild.id)
        if id in self.bot.banning_guilds and not percent:
            await ctx.send("Disabling random bans in this guild")
            self.bot.banning_guilds.pop(id)
        else:
            if not percent:
                percent = 0.00002
            elif not (0 < percent < 1):
                return await ctx.send("Error: Percentage must be from 0% to 100% (or 0.0 to 1.0)")
            await ctx.send(f"Enabling random bans in this guild with a {percent * 100}% chance")
            self.bot.banning_guilds[id] = percent
        safe_dump("data/banning.json", self.bot.banning_guilds)


def setup(bot):
    bot.add_cog(Settings(bot))
