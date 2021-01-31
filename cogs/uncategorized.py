import discord
from discord.ext import commands


from random import choice


songs = ["i-mWU2JFvUU", "alQei8zVMyM", "dpZ0wK48qKY", "HaM69OVOf74", "ng8mh6JUIqY", "whhTjySxxYE", "tlYU8mxXGnY",
         "U5w7tjrqDlo", "YEMEAxlYL04", "IoiaAA4vNaI", "9iHn_roIApY", "YZVJb1dyiV8", "MoN3zUJb6tA", "aXvG_Lx0Kp4",
         "eLoMej34zvA", "OZuW6BH_Vak", "4v8KEbQA8kw", "O0PV0M6-j9w", "mJag19WoAe0", "j_JaDDcyIIU", "W-0qx0yf_Hg",
         "BJhMjuza_1A", "W1LsRShUPtY", "Eq7-DsMhLaA", "AjZrV4wbdnQ", "VkuY33xb6v8", "MYKbQVw80mI", "4gNR7UDSLXo",
         "bRLML36HnzU", "ha0icvcByDs", "j_nuOyxMrMQ", "S7Jw_v3F_Q0", "KXrgF30VplE", "hTkW8DLVpwA", "tKJwvQfraY8",
         "j9BcQcFVcRM", "hCuMWrfXG4E", "oe2hdbft5-U", "Es5mh7pBeec", "aJfgHSUlr-s", "eYNMcolpHEM", "L3YwMmJgszI"]


class Uncategorized(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["support", "info"])
    async def information(self, ctx):
        embed = discord.Embed(
            name="Awesome?",
            description=f"""[GitHub](https://github.com/ernieIzde8ski/ratbot)
            [Bot Invite](https://discordapp.com/api/oauth2/authorize?client_id=466737001832382464&permissions=8&scope=bot)
            ["Support Server"](https://discord.gg/cHZYahK)
            [Good song](https://www.youtube.com/watch?v={choice(songs)})
            """
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Uncategorized(bot))
