import json
from configs import secrets
from datetime import datetime
import random
from typing import Optional

import aiohttp
import discord
import discord.ext.commands as commands
from pytz import timezone


def match_temp(temperature: float):
    temperatures = [[-40, "siberia"], [-20, "subuntwenty"], [-10, "subunten"], [0, "subzero"], [10, "subten"],
                    [20, "subtwenty"], [25, "sub25"], [30, "subthirty"], [35, "sub35"]]
    for temp, name in temperatures:
        if temperature <= temp:
            return name
    else:
        return "post35"


class Armenium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("cogs/on_member_update/Armenium.json", "r", encoding='utf-8') as f:
            self.data = json.load(f)

    @staticmethod
    async def get_temperature(city):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"http://api.openweathermap.org/data/2.5/weather?appid={secrets.weather_api_key}&q={city}") as resp:
                weather_data = await resp.json()  # get data as json
                temperature = round(weather_data['main']['temp'] - 273.15)  # get temperature & convert from Kelvin
                return temperature

    async def message(self, auth_id: int):
        temperature = await self.get_temperature(self.data['ids'][str(auth_id)]["city"])
        message = (
            f"__**Zdavstuy**__ \n\n" 
            f"{random.choice(self.data['msg']['greeting'])}, {random.choice(self.data['ids'][str(auth_id)]['nicknames'])}, "
            "hope you have Exciting Day. (Just kidding your Stupid) \n\n"
            f"It is currently {temperature} degrees Celsius outside for you. "
            f"{self.data['msg']['temp'][match_temp(temperature)]} \n\n"
            f"**{''.join(f'{sentence} ' for sentence in random.sample(self.data['msg']['russian'], random.randint(2, 4)))}**"
        )
        return message

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        ID = str(after.id)
        if after.id not in self.data["ids"]["raw_ids"]:
            return
        elif before.raw_status != "offline" or after.raw_status == "offline":
            return
        # Fair warning:
        # due to the nature of on_member_update and the following few lines,
        # the bot is guaranteed to spam your console logs if your client
        # has a few mutual servers with the bot, or you leave this unmodified
        elif self.data["ids"][ID]["reset_date"] == str(datetime.now(tz=timezone("US/Hawaii")))[:10]:
            print(f"{after} online, but already sent the message today")
            return
        else:
            self.data["ids"][ID]["reset_date"] = f"{datetime.now(tz=timezone(self.data['ids'][ID]['tz'])):%Y-%m-%d}"
            with open("cogs/on_member_update/Armenium.json", "w") as f:
                json.dump(self.data, f, indent=2)
            message = await self.message(after.id)
            await after.send(message)
            return

    @commands.command(aliases=["add_brogle", "add_arm"])
    @commands.is_owner()
    async def add_user_to_Armenium(self, ctx, user: discord.User, *, user_dict: str):
        """Command to add user to the list of weather updates
        Parameters:
            user: a discord user (id, mention, username, etc)
            user_dict: information on the user, in the format:
                {
                    "city": "a city",
                    "tz": "a timezone from pytz",
                    "reset_date": "None",
                    "nicknames": ["a", "list", "of", "nicknames"]
                }
            """
        user_dict = json.loads(user_dict)
        if user.id not in self.data["ids"]["raw_ids"]:
            self.data["ids"]["raw_ids"].append(user.id)
        self.data["ids"][str(user.id)] = user_dict
        with open("cogs/on_member_update/Armenium.json", "w") as file:
            json.dump(self.data, file, indent=2)
        await ctx.channel.send("Hopefully done")


def setup(bot):
    bot.add_cog(Armenium(bot))
