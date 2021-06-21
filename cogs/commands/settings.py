from typing import Optional
from discord.ext import commands

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
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

def setup(bot):
    bot.add_cog(Settings(bot))