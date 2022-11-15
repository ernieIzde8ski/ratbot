from typing import TYPE_CHECKING

from discord import Embed, Permissions
from discord.ext import commands
from discord.utils import oauth_url
from settings import settings
from utils import RatCog, RatCtx

INVITE_PERMISSIONS = Permissions(
    kick_members=True,
    ban_members=True,
    read_messages=True,
    send_messages=True,
    send_messages_in_threads=True,
    send_tts_messages=True,
    manage_messages=True,
    embed_links=True,
    attach_files=True,
    use_external_emojis=True,
    use_external_stickers=True,
    add_reactions=True,
)


class Informatics(RatCog):
    async def on_ready_hook(self):
        if TYPE_CHECKING:
            assert self.bot.user

        invite = oauth_url(self.bot.user.id, permissions=INVITE_PERMISSIONS)
        self.invite_msg = (
            f"Normal Invite: {invite}\n"
            f"Powerful Invite: {oauth_url(self.bot.user.id, permissions=Permissions(8))}"
        )
        self.info_embed_base = Embed(
            title="Hidden Rat Knowledge",
            description=(
                f"[Bot Invite]({invite})\n"
                f"[Server Invite]({settings.guild_invite})\n"
                f"[GitHub Repository]({settings.github_repo})\n"
                "[Random Music]({music})"
            ),
        )

    @commands.hybrid_command()
    async def invite(self, ctx: RatCtx):
        """Return bot invite URL"""
        await ctx.send(self.invite_msg)

    @commands.hybrid_command(aliases=("links", "information", "invites"))
    async def info(self, ctx: RatCtx):
        """Return various support URLs"""
        # define embed
        embed = self.info_embed_base.copy()
        if TYPE_CHECKING:
            assert isinstance(embed.description, str)
        embed.description = embed.description.format(music=settings.random_music)
        embed.color = ctx.me.color

        # send embed
        await ctx.send(embed=embed)


setup = Informatics.basic_setup
