import json
from configs import secrets
from datetime import datetime
import random
from typing import Optional

import aiohttp
from discord import User
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
                    f"https://api.openweathermap.org/data/2.5/weather?appid={secrets.weather_api_key}&q={city}") as resp:
                weather_data = await resp.json()  # get data as json
                true_temperature = round(weather_data['main']['temp'] - 273.15)        # get temperature & convert from Kelvin
                felt_temperature = round(weather_data['main']['feels_like'] - 273.15)  # get felt temperature
                return true_temperature, felt_temperature

    async def message(self, auth_id: int):
        temperatures = await self.get_temperature(self.data['ids'][str(auth_id)]['city'])
        true_temp = temperatures[0]
        felt_temp = temperatures[1]

        message = (
            f"__**Zdavstuy**__ \n\n" 
            f"{random.choice(self.data['greetings'])}, {random.choice(self.data['ids'][str(auth_id)]['nicknames'])}, "
            "hope you have Exciting Day. (Just kidding your Stupid) \n\n"
            f"It is currently {true_temp} degrees Celsius outside for you"
            + (f" (and it feels like {felt_temp})" if felt_temp != true_temp else "")
            + f". {self.data['temps'][match_temp(felt_temp)]} \n\n"
            f"**{''.join(f'{sentence} ' for sentence in random.sample(self.data['russian'], random.randint(2, 4)))}**"
        )
        return message

    def checks(self, ID, before, after):
        # fail check if not the right server
        if after.guild.id != self.data['ids']['guild_id']:
            return True
        # fail check if not a user
        if after.id not in self.data['ids']['raw_ids']:
            return True
        # fail check if not going from offline to online
        if before.raw_status != "offline" or after.raw_status == "offline":
            return True
        # fail check if message has already been sent
        today = f"{datetime.now(tz=timezone(self.data['ids'][ID]['tz'])):%Y-%m-%d}"
        if self.data["ids"][ID]["reset_date"] == today:
            return True
        # succeed check if all other conditions pass
        return False

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        ID = str(after.id)
        # makes sure that it only will send given a certain set of conditions
        if self.checks(ID, before, after):
            return
        # log message being sent today
        today = f"{datetime.now(tz=timezone(self.data['ids'][ID]['tz'])):%Y-%m-%d}"
        self.data["ids"][ID]["reset_date"] = today
        with open("cogs/on_member_update/Armenium.json", "w") as f:
            json.dump(self.data, f, indent=2)
        message = await self.message(after.id)
        await after.send(message)

    @commands.command(aliases=["add_brogle", "add_arm"])
    @commands.is_owner()
    async def add_user_to_Armenium(self, ctx, user: User, *, user_dict: str):
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
