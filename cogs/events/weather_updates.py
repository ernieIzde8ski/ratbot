import asyncio
import random
from datetime import datetime
from functools import cache
from typing import Optional, Union

import discord
from discord.ext import commands
from pytz import timezone as tz
from utils._types import Russian, WeatherResps, WeatherUsers
from utils.classes import RatBot
from utils.converters import FlagConverter
from utils.functions import safe_dump, safe_load
from utils.weather_retrieval_types import WeatherResponseError, WeatherResponseType

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


def log_if_pp(pos: str | int, id: str) -> None:
    return None
    # if id == 282307423530647562:
    #     print("[6PP IDENTIFIED]", pos)


UTC = tz("UTC")


def get_tz(_tz: str = None):
    if _tz is None:
        return UTC
    return tz(_tz)


class WeatherUpdates(commands.Cog):
    def __init__(self, bot: RatBot):
        self.bot = bot
        self.bot.load_weather("")
        self.bible: Russian = safe_load("data/russian.json", [])
        self.resps: WeatherResps = safe_load("data/weather_resps.json", {})
        self.users: WeatherUsers = safe_load("data/weather_users.json", {"active_users": [], "_": {}})

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

        current, felt, _max, _min = (
            round(weather["main"][key], 1) for key in ["temp", "feels_like", "temp_max", "temp_min"]
        )
        evaluation = self.temp_eval(self.to_celsius(current, weather["units"]["temp"]))

        message = FORMAT_UNFELT if current == felt else FORMAT_FELT

        return message.format(
            GREETING=greeting,
            TEMP=current,
            TEMP_UNIT=weather["units"]["temp"],
            FELT=felt,
            LOCAL_MAXIMUM=_max,
            LOCAL_MINIMUM=_min,
            WEATHER_DESCRIPTION=weather["weather"][0]["description"].title(),
            HUMIDITY=weather["main"]["humidity"],
            WIND=weather["wind"]["speed"],
            WIND_UNIT=weather["units"]["speed"],
            EVALUATION=evaluation,
            RUSSIAN=russian,
        )

    def message_constructor(self, user: dict, weather: WeatherResponseType | WeatherResponseError) -> str:
        fn = self.err_msg_ctr if weather.get("error") else self.true_msg_ctr
        return fn(user, weather)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, member: discord.Member):
        id = str(member.id)
        if member.bot:
            return log_if_pp("Bot", id)
        elif self.bot.weather.locs.get(id) is None:
            return log_if_pp("Weather Locations", id)
        elif member.id not in self.users["active"]:
            return log_if_pp("Not in Active Users", id)
        elif before.raw_status != "offline" or member.raw_status == "offline":
            return log_if_pp("Status Ineligible", id)

        now = datetime.now(tz=get_tz(self.users["_"][id].get("tz"))).strftime("%d-%m-%Y")
        if self.users[id].get("sent") == now:
            return

        weather = await self.bot.weather.get_weather(**self.bot.weather.locs[id])
        self.users["_"][id]["sent"] = now
        safe_dump("data/weather_updates.json", self.users)
        msg = self.message_constructor(self.users[id], weather)
        try:
            await member.send(msg)
        except discord.Forbidden:
            return await self.bot.status_channels.DM.send(f"{member} might have me blocked 😦")

        if random.random() < 0.1:
            _m = await member.send("do you want a Song ?")

            def _check(m):
                if m.channel != _m.channel or m.author == _m.author:
                    return False
                if not m.content:
                    return False
                return m.content.lower()[0] in ["y", "n"]

            try:
                message = await self.bot.wait_for("message", timeout=300.0, check=_check)
            except asyncio.TimeoutError:
                return await member.send(
                    "WHAT IS WRONG WTIH YOU ARE YOU STUPID AOR SOMETHING . OR ARE YOU JUST STUPID OR ARE YOU"
                )

            await asyncio.sleep(1)
            value = message.content.lower()[0]
            if value == "y":
                await member.send(random.choice(["Awsom", "Based", "Yes", "Yea", "Good", "Here"]))
                await member.send("https://youtu.be/" + random.choice(self.bot.data.songs))
            elif value == "n":
                await member.send(random.choice(["Rude", "Dam", "Cringe ?", "Troled"]))

    @commands.command(aliases=["wset"])
    @commands.is_owner()
    async def weather_data_set(
        self, ctx: commands.Context, target: Optional[Union[discord.Member, discord.User]], *, flags: FlagConverter = {}
    ):
        """
        Add a user to weather updates
        tzs: https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
        Usage: r;wset --id 302956027656011776 --tz America/Los_Angeles --aliases ["ernie", "Pepito"]
        If no flags are provided, then this attempts to remove them from active_users.
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
            if key not in self.users["active"]:
                self.users["active"].append(key)
        elif key in self.users["active"]:
            self.users["active"].remove(key)
        # Exception raised when flags are not present (not counting
        # ID flag) and the target is not currently an active user
        else:
            raise commands.BadArgument("Target is not an active user")

        # Save information
        safe_dump("data/weather_updates.json", self.users)
        await ctx.send(f"Updated user data for {key}")


def setup(bot: RatBot):
    bot.add_cog(WeatherUpdates(bot))
