import discord.ext.commands as commands


async def f_to_c(degrees_f: float):
    return (degrees_f - 32) * 5 / 9


async def c_to_k(degrees_c: float):
    return degrees_c + 273.15


async def f_to_k(degrees_f: float):
    degrees_c = await f_to_c(degrees_f)
    return await c_to_k(degrees_c)

async def r_to_k(degrees_r: float):
    return degrees_r * 5 / 9

class Temperature(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temps = {"fahrenheit": ["f", "fahrenheit", "cringe"],
                      "celsius": ["c", "celsius", "centigrade", "based"],
                      "kelvin": ["k", "kelvin", "plusbased"],
                      "rankine": ['r', 'rankine', 'doubleplusbased']}
        self.temps_list = []
        for iter_1 in self.temps:
            for iter_2 in self.temps.get(iter_1):
                self.temps_list.append(iter_2)

    @commands.command(aliases=["conv", "temp", "temperature"])
    async def convert(self, ctx, degree: float, unit: str):
        """Converts from celsius and fahrenheit temperatures
        Parameters:
            unit: fahrenheit, celsius
            degree: degree in respective unit"""
        unit = unit.lower()
        if unit not in self.temps_list:
            return await ctx.send("please enter a Unit parameter Correctly")

        if unit in self.temps['fahrenheit']:
            await ctx.send(f"{round(await f_to_k(degree), 2)}°")
        elif unit in self.temps['celsius']:
            await ctx.send(f"{round(await c_to_k(degree), 2)}°")
        elif unit in self.temps['kelvin']:
            await ctx.send("This is already in plusbasedform Bupid\n"
                           f"{round(degree, 2)}°")
        elif unit in self.temps['rankine']:
            await ctx.send("Ok Lowering from doubleplusbased to plusbased\n"
                           f"{round(await r_to_k(degree), 2)}°")


def setup(bot):
    bot.add_cog(Temperature(bot))
