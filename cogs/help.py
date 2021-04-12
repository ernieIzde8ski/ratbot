from random import choice

from discord import Embed, Permissions, utils, errors
from discord.ext import commands


class Help(commands.Cog):
    """There is only one command here Doe?
    Yea"""

    def __init__(self, bot):
        self.bot = bot

    async def embed_constructor(self, ctx):
        bot_owner = (await commands.Bot.application_info(self.bot)).owner
        return Embed(
            name="Lol?",
            description=f"[GitHub](https://github.com/ernieIzde8ski/ratbot)\n"
                        f"[Invitame]({utils.oauth_url(self.bot.user.id, permissions=Permissions(8))})\n"
                        f"[invitación pero necesitas pensar]({utils.oauth_url(self.bot.user.id, permissions=Permissions(201714752))})\n"
                        f"[\"Support Server\"](https://discord.gg/cHZYahK)\n"
                        f"[Good song](https://www.youtube.com/watch?v={choice(self.bot.config.songs)})",
            color=ctx.author.color,
            timestamp=ctx.message.created_at
        ).set_author(
            name=f"— {bot_owner}",
            icon_url=bot_owner.avatar_url
        ).set_footer(
            text=f"Bitch command No extra help for you beyond '{self.bot.config.prefix[0]}help commands'"
        )

    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        """Provides general/support information"""
        try:
            await ctx.send(embed=await self.embed_constructor(ctx))
        except errors.Forbidden as e:
            ayuda = self.bot.help_command
            ayuda.context = ctx
            await ctx.channel.send(await ayuda.command_callback(ctx))
            await ctx.channel.send(f"Command raised an exception: Forbidden: {e}\n"
                                   f"If You Happen To Want The Other Help Command Please Permit The Bot"
                                   f"To Having The Embed Permissions")

    @help.command(aliases=["cmd", "cmds", "command"])
    async def commands(self, ctx):
        """built-in help command"""
        ayuda = self.bot.help_command
        ayuda.context = ctx
        await ctx.channel.send(await ayuda.command_callback(ctx))


def setup(bot):
    bot.remove_command("help")
    print("Saying the Bye-Bye to Help Command")
    bot.add_cog(Help(bot))
