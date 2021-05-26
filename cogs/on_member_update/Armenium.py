import json
import random
from asyncio import sleep
from asyncio.exceptions import TimeoutError
from datetime import datetime
from typing import Optional, Union

import aiohttp
import discord.ext.commands as commands
from discord import User
from pytz import timezone

from configs.secrets import weather_api_key as apikey


def match_temp(temperature: float) -> str:
    temperatures = (
        [-40, "siberia"], [-30, "sub-30"], [-20, "sub-20"], [-15, "sub-15"], [-10, "sub-10"], [-5, "sub5"], [0, "sub0"],
        [5, "sub5"], [10, "sub10"], [15, "sub15"], [20, "sub20"], [25, "sub25"], [30, "sub30"], [35, "sub35"],
        [40, "sub40"]
    )
    for temp, name in temperatures:
        if temperature <= temp:
            return name
    else:
        return "post40"


def match_wind(speed: float) -> str:
    winds = (
        [0.45, "Calm"], [1.34, "Light Air"], [3.13, "Light Breeze"], [5.36, "Gentle Breeze"], [8.05, "Moderate Breeze"],
        [10.73, "Fresh Breeze"], [13.86, "Strong Breeze"], [16.99, "Near Gale"], [20.56, "Gale"],
        [24.14, "Severe Gale"], [28.16, "Storm"], [32.19, "Violent Storm"], [42.49, "Cat. 1 Hurricane"],
        [49.17, "Cat. 2 Hurricane"], [57.67, "Cat. 3 Hurricane"], [69.74, "Cat. 4 Hurricane"]
    )
    for windspeed, name in winds:
        if speed <= windspeed:
            return name
    else:
        return "Cat. 5 Hurricane"


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

    async def message_constructor(self, auth_id: Union[int, str]) -> str:
        auth_id = str(auth_id)
        city = self.data[auth_id]['city']
        temps = await self.get_temperature(city)

        title = "Zdavstuy"
        greeting = random.choice(self.msg['greetings'])
        nick = random.choice(self.data[auth_id]['nicknames'])
        temperature = f"It is currently {temps['true']} degrees Celsius outside"
        if temps['true'] != temps['felt']: temperature += f" (and it feels like {temps['felt']})"
        weather = f"The Wind is going at {temps['wind']} Meter per second ({match_wind(temps['wind'])}) " \
                  f"& the weather is `{temps['weather']}`"
        temperature_analysis = self.msg['temps'][match_temp(temps['felt'])]
        russian = " ".join(f'{sentence} ' for sentence in random.sample(self.msg['russian'], random.randint(3, 5)))

        message = f"__**{title}**__\n\n" \
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

    async def send_song(self, victim: User):
        if random.random() < 0.933: return
        await sleep(1)
        await victim.send("do you want Song ?")
        try:
            def check(msg):
                # prevent errors for when msg.content is None or when not in direct messages
                if not msg.content or msg.guild: return False
                return msg.author == victim and msg.content[0].lower() in ["y", "n"]

            message = await self.bot.wait_for("message", timeout=180, check=check)
        except TimeoutError:
            return await victim.send("Rude")
        else:
            if message.content[0].lower() == "n":
                await victim.send(random.choice(("WTF.", "Dam", "Wered", "OK Lol", "Owned", "Yea")))
            else:
                await victim.send("Awsom")
                await victim.send(f"https://youtu.be/{random.choice(list(self.bot.config.songs))}")

    @commands.Cog.listener()
    async def on_member_update(self, before, member):
        ID = str(member.id)
        # makes sure that it only will send given a certain set of conditions
        if self.checks(ID, before, member):
            return

        # send message
        message = await self.message_constructor(member.id)
        await member.send(message)

        # log message being sent today
        today = f"{datetime.now(tz=timezone(self.data[ID]['tz'])):%Y-%m-%d}"
        self.data[ID]['reset_date'] = today
        with open("cogs/on_member_update/ids.json", "w") as f:
            json.dump(self.data, f)

        await self.send_song(member)

    @commands.command(aliases=["sa"])
    @commands.is_owner()
    async def send_Armenium(self, ctx, victim: Optional[User]):
        """For testing"""
        victim = victim if victim else ctx.author
        message = await self.message_constructor(victim.id)
        await victim.send(message)
        await self.send_song(victim)

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
        with open("cogs/on_member_update/ids.json", "w") as file:
            json.dump(self.data, file)
        await ctx.channel.send("Hopefully done")


def setup(bot):
    bot.add_cog(Armenium(bot))
