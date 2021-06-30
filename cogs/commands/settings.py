from discord.ext import commands
from modules._json import safe_load, safe_dump
from modules.converters import Percentage
from typing import Optional


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tenor_guilds = set(safe_load("data/tenor_guilds.json", []))
        self.bot.banning_guilds = safe_load("data/banning.json", {})

    @commands.command(aliases=["prefix"])
    @commands.has_permissions(manage_guild=True)
    async def set_prefix(self, ctx, prefix: Optional[str]):
        if not ctx.guild:
            return await ctx.send("You must be in a guild to run this command!")
        if not prefix:
            return await ctx.send("Your prefix must have a length!")
        self.bot.dispatch("prefix_update", str(ctx.guild.id), prefix)
        prefix = prefix.replace("`", "\`")
        await ctx.send(f"Updated prefix to {prefix}")

    @commands.command(aliases=["toggle_tenors"])
    @commands.has_permissions(manage_guild=True)
    async def tenor_toggle(self, ctx):
        if not ctx.guild:
            return await ctx.send("You must be in a guild to run this command!")

        if ctx.guild.id in self.bot.tenor_guilds:
            await ctx.send("Disabling tenor slaying in this server")
            self.bot.tenor_guilds.remove(ctx.guild.id)
        else:
            await ctx.send("Enabling tenor slaying in this server")
            self.bot.tenor_guilds.add(ctx.guild.id)
        safe_dump("data/tenor_guilds.json", list(self.bot.tenor_guilds))
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def toggle_random_bans(self, ctx, percent: Optional[Percentage]):
        if not ctx.guild:
            return await ctx.send("You need to be in a guild for this!")

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
