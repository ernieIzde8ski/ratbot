import discord.ext.commands as commands


async def fahrenheit_to_celsius(degrees_f: float):
    return (degrees_f - 32) * 5 / 9


async def celsius_to_kelvin(degrees_c: float):
    return degrees_c + 273.15


async def fahrenheit_to_kelvin(degrees_f: float):
    degrees_c = await fahrenheit_to_celsius(degrees_f)
    return await celsius_to_kelvin(degrees_c)


class Temperature(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fahrenheit_list = ["f", "fahrenheit", "cringe"]
        self.celsius_list = ["c", "celsius", "centigrade", "based"]
        self.kelvin_list = ["k", "kelvin", "plusbased"]

    @commands.command()
    async def convert(self, ctx, degree: float, original_unit: str):
        """Converts from celsius and fahrenheit temperatures
        Parameters:
            original_unit: fahrenheit, celsius
            degree: degree in respective unit"""
        if original_unit.lower() in self.fahrenheit_list:
            return await ctx.channel.send(f"{round(await fahrenheit_to_kelvin(degree), 2)}°")
        elif original_unit.lower() in self.celsius_list:
            return await ctx.channel.send(f"{round(await celsius_to_kelvin(degree), 2)}°")
        elif original_unit.lower() in self.kelvin_list:
            return await ctx.channel.send("This is already in plusbasedform Bupid")
        else:
            return await ctx.channel.send("please enter a Unit parameter Correctly")


def setup(bot):
    bot.add_cog(Temperature(bot))
