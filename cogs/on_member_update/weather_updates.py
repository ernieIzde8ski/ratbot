from discord.ext import commands
from discord import Member

from modules.converters import FlagConverter
from modules._json import safe_dump, safe_load

import random
from typing import Optional, Union
from modules.weather import get_weather

from datetime import datetime
from pytz import timezone as tz


class WeatherUpdates(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bible = safe_load("data/russian.json", [])
        self.data = safe_load("data/weather_resps.json", {})
        self.users = safe_load("data/weather_updates.json", {"active_users": []})
        self.user_locations = safe_load("data/weather_locations.json", {})

    @commands.Cog.listener()
    async def on_weather_users_update(self, new_obj):
        self.user_locations = new_obj

    def check(self, member: Member):
        return member.bot or member.guild.id != self.bot.config["main_guild"] or not (self.user_locations.get(str(member.id)) and member.id in self.users["active_users"])

    def temp_eval(self, temp: Union[int, float]) -> str:
        for num, value in self.data["temperature_resps"]:
            if temp <= num:
                return value
        else:
            return "You managed to not have an evaluation . Wtf"

    def message_constructor(self, user: dict, weather: dict) -> str:
        message = "__**Zdavstuy**__ \n\n"
        message += random.choice(self.data["greetings"]
                                 ).format(random.choice(user["aliases"]))
        message += " hope you have Exciting Day. (Just kidding your Stupid)\n\n"
        if weather.get("error"):
            message += f"Error occured (Because you are Stupid) (`{weather['error']}`). " \
                        "Try resetting your Location data (using `r.w set $CITY_NAME`) and trying again tomorrow (Not today (Stupid idiot thing)) \n\n"
        else:
            [current, felt, high, low] = [round(weather['main']['temp'], 1), round(
                weather['main']['feels_like'], 1), round(weather['main']['temp_max'], 1), round(weather['main']['temp_min'], 1)]
            felt = f" (and it feels like {felt}°)" if current != felt else ""

            message += f"It is currently {current} degrees {weather['units']['temp']}{felt}, with a high of {high}° and a low of {low}°. " \
                       f"the Weather is \"{weather['weather'][0]['description'].title()}\", " \
                       f"with a humidity at {weather['main']['humidity']}% and windspeeds at {weather['wind']['speed']} {weather['units']['speed']}. "

            if weather['units']['temp'] == "Fahrenheit":
                current = (current - 32) * (5/9)
            elif weather['units']['temp'] == "Kelvin":
                current -= 273.15
            message += self.temp_eval(current) + "\n\n"
        
        message += "**" + " ".join(random.sample(self.bible, k = random.randint(2, 5))) + "**"

        return message

    @commands.Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        id = str(after.id)
        if self.check(after):
            return
        elif before.raw_status != "offline" or after.raw_status == "offline":
            return
        now = datetime.now(tz=tz(self.users[id]["tz"])).strftime("%d-%m-%Y")
        if self.users[id].get("sent") == now:
            return
        else:
            weather = await get_weather(self.bot.config["weather"], **self.user_locations[id])
            await after.send(self.message_constructor(self.users[id], weather))
            self.users[id]["sent"] = now
            safe_dump("data/weather_updates.json", self.users)

    @commands.command(aliases=["wset"])
    @commands.is_owner()
    async def weather_data_set(self, ctx, target: Optional[Member], *, flags: FlagConverter = {}):
        """
        Add a user to weather updates
        Usage: r;wset --id 302956027656011776 --tz America/Los_Angeles --aliases ["ernie", "Pepito"]
        """
        if target:
            target = target.id
        elif flags.get("id"):
            target = flags.pop("id")
        else:
            return await ctx.send("Invalid user!")

        self.users[str(target)] = flags
        self.users[str(target)]["sent"] = False
        if target not in self.users["active_users"]:
            self.users["active_users"].append(target)
        safe_dump("data/weather_updates.json", self.users)
        await ctx.send(f"Updated user data for {target}")


def setup(bot):
    bot.add_cog(WeatherUpdates(bot))
