from discord.ext import commands
from typing import Optional
from modules._json import safe_load, safe_dump


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.tenor_guilds = set(safe_load("data/tenor_guilds.json", []))

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

    @commands.command(aliases=["toggle_tenor"])
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


def setup(bot):
    bot.add_cog(Settings(bot))
