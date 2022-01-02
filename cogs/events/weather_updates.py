import asyncio
import random
from datetime import datetime
from functools import cache
from typing import Optional, TypedDict, Union

import discord
from discord.ext import commands
from pytz import timezone as tz
from utils.classes import RatBot
from utils.converters import FlagConverter
from utils.functions import safe_dump, safe_load
from utils.weather_types import WeatherResponseError, WeatherResponseType

FORMAT_ERROR = """
__**Здавстуй**__

{GREETING} hope you have Exciting Day. (Just kidding your Stupid)

Error occured (Because you are Stupid) (`{ERROR}`). Try resetting your Location data (using `r.w set $CITY_NAME`) and trying again tomorrow (Not today (Stupid idiot thing))

**{RUSSIAN}**
""".strip()

FORMAT_UNFELT = """
__**Здавстуй**__

{GREETING} hope you have Exciting Day. (Just kidding your Stupid)

It is currently {TEMP} degrees {TEMP_UNIT}, with a local maximum of {LOCAL_MAXIMUM}° and a local  of {LOCAL_MINIMUM}°. the Weather is {WEATHER_DESCRIPTION}, with a humidity at {HUMIDITY}% and windspeeds at {WIND} {WIND_UNIT}. {EVALUATION}

**{RUSSIAN}**
""".strip()
FORMAT_FELT = """
__**Здавстуй**__

{GREETING} hope you have Exciting Day. (Just kidding your Stupid)

It is currently {TEMP} degrees {TEMP_UNIT} (and it feels like {FELT}°), with a local maximum of {LOCAL_MAXIMUM}° and a local  of {LOCAL_MINIMUM}°. the Weather is {WEATHER_DESCRIPTION}, with a humidity at {HUMIDITY}% and windspeeds at {WIND} {WIND_UNIT}. {EVALUATION}

**{RUSSIAN}**
""".strip()


class WeatherResponses(TypedDict):
    greetings: list[str]
    temperature_resps: list[tuple[int, str]]


class WeatherUpdates(commands.Cog):

    def __init__(self, bot: RatBot):
        self.bot = bot
        self.bot.load_weather("")
        self.bible = safe_load("data/russian.json", [])
        self.resps: WeatherResponses = safe_load("data/weather_resps.json", {})
        self.users = safe_load("data/weather_updates.json", {"active_users": []})

    def check(self, member: discord.Member) -> bool:
        """Returns true if a member should not be checked."""
        return (
            member.bot
            or not self.bot.weather.locs.get(str(member.id))
            or member.id not in self.users["active_users"]
        )

    @staticmethod
    @cache
    def to_celsius(num: int | float, _from: str) -> float:
        """Converts a unit to celsius. If _from is invalid, returns input."""
        _from = _from and _from[0].lower()
        if _from == "f":
            return (num - 32) * (5 / 9)
        elif _from in ["k", "s"]:
            return num - 273.15
        return num

    def temp_eval(self, temp: int | float) -> str:
        for num, value in self.resps["temperature_resps"]:
            if temp <= num:
                return value
        else:
            return "You managed to not have an evaluation . Wtf"

    def err_msg_ctr(self, user: dict, err: WeatherResponseError) -> str:
        greeting = random.choice(self.resps["greetings"]).format(random.choice(user["aliases"]))
        russian = " ".join(random.sample(self.bible, k=random.randint(2, 5)))
        return FORMAT_ERROR.format(GREETING=greeting, ERROR=err["error"], RUSSIAN=russian)

    def true_msg_ctr(self, user: dict, weather: WeatherResponseType) -> str:
        greeting = random.choice(self.resps["greetings"]).format(random.choice(user["aliases"]))
        russian = " ".join(random.sample(self.bible, k=random.randint(2, 5)))

        current, felt, _max, _min = (round(weather["main"][key], 1) for key in ["temp", "feels_like", "temp_max", "temp_min"])
        evaluation = self.temp_eval(self.to_celsius(current, weather["units"]["temp"]))

        message = FORMAT_UNFELT if current == felt else FORMAT_FELT

        return message.format(
            GREETING=greeting,
            TEMP=current, TEMP_UNIT=weather["units"]["temp"], FELT=felt, LOCAL_MAXIMUM=_max, LOCAL_MINIMUM=_min,
            WEATHER_DESCRIPTION=weather["weather"][0]["description"].title(),
            HUMIDITY=weather["main"]["humidity"],
            WIND=weather["wind"]["speed"], WIND_UNIT=weather["units"]["speed"],
            EVALUATION=evaluation,
            RUSSIAN=russian
        )

    def message_constructor(self, user: dict, weather: WeatherResponseType | WeatherResponseError) -> str:
        fn = self.err_msg_ctr if weather.get("error") else self.true_msg_ctr
        return fn(user, weather)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        id = str(after.id)
        if self.check(after):
            return
        elif before.raw_status != "offline" or after.raw_status == "offline":
            return
        now = datetime.now(tz=tz(self.users[id]["tz"])).strftime("%d-%m-%Y")
        if self.users[id].get("sent") == now:
            return

        weather = await self.bot.weather.get_weather(**self.bot.weather.locs[id])
        self.users[id]["sent"] = now
        safe_dump("data/weather_updates.json", self.users)
        msg = self.message_constructor(self.users[id], weather) if not weather.get("error") else self.err_msg_ctr(self.users[id], weather)
        try:
            await after.send(msg)
        except discord.Forbidden:
            return await self.bot.status_channels.DM.send(f"{after} might have me blocked 😦")

        if random.random() < 0.1:
            _m = await after.send("do you want a Song ?")

            def _check(m):
                if m.channel != _m.channel or m.author == _m.author:
                    return False
                if not m.content:
                    return False
                return m.content.lower()[0] in ["y", "n"]

            try:
                message = await self.bot.wait_for("message", timeout=300.0, check=_check)
            except asyncio.TimeoutError:
                return await after.send("WHAT IS WRONG WTIH YOU ARE YOU STUPID AOR SOMETHING . OR ARE YOU JUST STUPID OR ARE YOU")

            await asyncio.sleep(1)
            value = message.content.lower()[0]
            if value == "y":
                await after.send(random.choice(["Awsom", "Based", "Yes", "Yea", "Good", "Here"]))
                await after.send("https://youtu.be/" + random.choice(self.bot.data.songs))
            elif value == "n":
                await after.send(random.choice(["Rude", "Dam", "Cringe ?", "Troled"]))

    @commands.command(aliases=["wset"])
    @commands.is_owner()
    async def weather_data_set(self, ctx: commands.Context, target: Optional[Union[discord.Member, discord.User]], *, flags: FlagConverter = {}):
        """
        Add a user to weather updates
        tzs: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
        Usage: r;wset --id 302956027656011776 --tz America/Los_Angeles --aliases ["ernie", "Pepito"]
        """
        if target:
            key = str(target.id)
        elif flags.get("id"):
            key = str(flags.pop("id"))
        else:
            raise commands.BadArgument("Could not get target user")

        # Add a user if flags are present
        # otherwise, try to remove a user
        if flags:
            self.users[key] = flags
            self.users[key]["sent"] = False
            if key not in self.users["active_users"]:
                self.users["active_users"].append(key)
        elif key in self.users["active_users"]:
            self.users["active_users"].remove(key)
        # Exception raised when flags are not present (not counting
        # ID flag) and the target is not currently an active user
        else:
            raise commands.BadArgument("Target is not an active user")

        # Save information
        safe_dump("data/weather_updates.json", self.users)
        await ctx.send(f"Updated user data for {key}")


def setup(bot: RatBot):
    bot.add_cog(WeatherUpdates(bot))
