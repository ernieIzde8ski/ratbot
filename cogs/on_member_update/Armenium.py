import json
import random
from datetime import datetime
from typing import Optional, Union

import aiohttp
import discord.ext.commands as commands
from configs.secrets import weather_api_key as apikey
from discord import User, Embed, Colour
from pytz import timezone


def match_temp(temperature: float) -> str:
    temperatures = (
        [-40, "siberia"], [-30, "sub-30"], [-20, "sub-20"], [-15, "sub-15"], [-10, "sub-10"], [-5, "sub5"], [0, "sub0"],
        [5, "sub5"],
        [10, "sub10"], [15, "sub15"], [20, "sub20"], [25, "sub25"], [30, "sub30"], [35, "sub35"], [40, "sub40"]
    )
    for temp, name in temperatures:
        if temperature <= temp:
            return name
    else:
        return "post40"


class Armenium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("cogs/on_member_update/ids.json", "r", encoding="utf-8") as f:
            self.data = json.load(f)
        with open("cogs/on_member_update/message_construction.json", "r", encoding="utf-8") as f:
            self.msg = json.load(f)

    @staticmethod
    async def get_temperature(city) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f"https://api.openweathermap.org/data/2.5/weather?appid={apikey}&q={city}&units=metric") as resp:
                weather_data = await resp.json()  # get data as json
                return {
                    "true": round(weather_data['main']['temp']),
                    "felt": round(weather_data['main']['feels_like']),
                    "wind": weather_data["wind"]["speed"],
                    "weather": weather_data["weather"][0]["description"].lower()
                }

    async def embed_constructor(self, auth_id: Union[int, str]) -> Embed:
        auth_id = str(auth_id)
        city = self.data[auth_id]['city']
        temps = await self.get_temperature(city)

        title = "Zdavstuy"
        greeting = random.choice(self.msg['greetings'])
        nick = random.choice(self.data[auth_id]['nicknames'])
        temperature = f"It is currently {temps['true']} degrees Celsius outside"
        if temps['true'] != temps['felt']: temperature += f" (and it feels like {temps['felt']})"
        weather = f"The Wind is going at {temps['wind']} Meter per second & the weather is `{temps['weather']}`"
        temperature_analysis = self.msg['temps'][match_temp(temps['felt'])]
        russian = " ".join(f'{sentence} ' for sentence in random.sample(self.msg['russian'], random.randint(3, 5)))

        message = f"**{title}**\n\n" \
                  f"{greeting}, {nick}, hope you have Exciting Day. (Just kidding your Stupid) \n\n" \
                  f"{temperature}. {weather}. {temperature_analysis}\n\n" \
                  f"**{russian}**"
        return message

    def checks(self, ID, before, after) -> bool:
        # fail check if not the right server or not a user
        if after.guild.id != self.data['guild_id'] or after.id not in self.data['raw_ids']:
            return True
        # fail check if not going from offline to online
        if before.raw_status != "offline" or after.raw_status == "offline":
            return True
        # fail check if message has already been sent
        today = f"{datetime.now(tz=timezone(self.data[ID]['tz'])):%Y-%m-%d}"
        if self.data[ID]["reset_date"] == today:
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
        today = f"{datetime.now(tz=timezone(self.data[ID]['tz'])):%Y-%m-%d}"
        self.data[ID]['reset_date'] = today
        with open("cogs/on_member_update/Armenium.json", "w") as f:
            json.dump(self.data, f, indent=2)
        embed = await self.embed_constructor(after.id)
        await after.send(embed=embed)

    @commands.command(aliases=["sa"])
    @commands.is_owner()
    async def send_Armenium(self, ctx, victim: Optional[User]):
        """For testing"""
        victim = victim if victim else ctx.author
        message = await self.embed_constructor(victim.id)
        await victim.send(message)

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
        if user.id not in self.data['raw_ids']:
            self.data['raw_ids'].append(user.id)
        self.data[str(user.id)] = user_dict
        with open("cogs/on_member_update/Armenium.json", "w") as file:
            json.dump(self.data, file, indent=2)
        await ctx.channel.send("Hopefully done")


def setup(bot):
    bot.add_cog(Armenium(bot))
