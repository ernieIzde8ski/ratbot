import discord.ext.commands as commands
import discord
import json
from random import choice
from datetime import datetime
from pytz import timezone
import secrets


def match_temp(temperature: float):
    temperatures = [[-40, "siberia"], [-20, "subuntwenty"], [-10, "subunten"], [0, "subzero"], [10, "subten"], [20, "subtwenty"], [25, "sub25"], [30, "subthirty"], [35, "sub35"]]
    for temp, name in temperatures:
        if temperature <= temp:
            return name
    else:
        return "post35"


async def get_temperature(city: str = "Irvine"):
    url = f"http://api.openweathermap.org/data/2.5/weather?appid={secrets.weather_api_key}&q="

class Armenium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("cogs/on_member_update/Armenium.json") as file:
            self.data = json.load(file)

    async def message(self):
        message = (
            f"__**Zdavstuy**__ \n\n"
            f"{choice(self.data['msg']['greeting'])}, {choice(self.data['msg']['nickname'])}, hope you have Exciting Day. (Just kidding your Stupid) \n\n"
            f"It is currently {WEATHER} degrees Celsius outside for you. {self.data['temp'][match_temp(WEATHER)]} \n\n"
            f"{choice(self.data['russian'])}"
        )
        return message

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if after.id != self.data["id"]:
            return
        elif before.raw_status != "offline" or after.raw_status == "offline":
            return
        elif self.data["reset_time"] == str(datetime.now(tz=timezone("US/Hawaii")))[:10]:
            return print(f"{after} online, but already sent the message today")
        else:
            self.data["reset_time"] = str(datetime.now(tz=timezone("US/Hawaii")))[:10]
            with open("cogs/on_member_update/Armenium.json") as file:
                json.dump(self.data, file, indent=2)
            message = await self.message()
            await after.send(message)


def setup(bot):
    bot.add_cog(Armenium(bot))
