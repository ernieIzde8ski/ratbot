import json
import logging
import random
from datetime import date, datetime
from os import getenv

from disnake import Member, Status
from owmpy.current import Client
from owmpy.utils import StandardUnits, convert_temp
from pydantic import ValidationError

from lib import Bot, Cog, dirs
from lib.ext.weather import MessageConfig, WeatherUser, get_message_template, getch_bible

weather_dir = dirs.weather_home()
message_template = get_message_template()


class Weather(Cog):
    bible: list[str]
    mconfig: MessageConfig
    users: dict[int, WeatherUser]

    def __init__(self, bot: Bot) -> None:
        weather_token = getenv("RATBOT_TOKEN_WEATHER")
        if weather_token is None:
            raise RuntimeError("$RATBOT_TOKEN_WEATHER is unset")
        self.client = Client(weather_token, bot.session)
        self.mconfig = MessageConfig.load_or_default()

        users: dict[int, WeatherUser] = {}

        for path in weather_dir.glob("*.json"):
            id_str = path.name.removesuffix("".join(path.suffixes))
            try:
                id = int(id_str)
                with open(path, "r") as file:
                    data = json.load(file)
                user = WeatherUser.model_validate(data)
                users[id] = user
            except ValidationError:
                logging.exception(f"weather user: failed to validate id {id_str}")
            except ValueError:
                logging.error(f"weather user: invalid id: {id_str}")

        if not users:
            raise RuntimeError("not a single weather user was loaded")
        else:
            self.users = users
            logging.info(f"Weather users: {sorted(users)}")

        super().__init__(bot)

    async def post_init_hook(self) -> None:
        self.bible = await getch_bible(self.session)

    async def prepare_message(self, user: WeatherUser) -> str:
        resp = await self.client.get(user.coords, units=user.preferred_units)
        quote_count = random.randint(self.mconfig.min_quotes, self.mconfig.max_quotes)
        assessment = self.mconfig.evaluate_temperature(
            convert_temp(resp.main.temp, resp.units, StandardUnits.METRIC)
        )

        return message_template.format(
            first_word=random.choice(self.mconfig.first_words),
            morning_greeting=random.choice(self.mconfig.morning_greeting),
            name=random.choice(user.aliases),
            temp_real=round(resp.main.temp, 2),
            temp_unit_long=resp.units.temp.long,
            temp_felt=round(resp.main.feels_like, 2),
            temp_unit_short=resp.units.temp.short,
            clouds_percent=resp.clouds.all,
            condition=resp.weather[0].description.title(),
            humidity=round(resp.main.humidity, 2),
            windspeed=resp.wind.speed,
            speed_unit_long=resp.units.speed.long,
            assessment=assessment,
            russian_text=" ".join(random.choices(self.bible, k=quote_count)),
        )

    @Cog.listener()
    async def on_presence_update(self, before: Member, after: Member) -> None:
        ### run checks before sending a message
        if after.id not in self.users:
            return
        if before.status != Status.offline or after.status not in (
            Status.dnd,
            Status.do_not_disturb,
            Status.online,
        ):
            return

        user = self.users[after.id]
        if after.guild.id != user.watched_guild or not user.enabled:
            return

        today: date = (datetime.now(user.timezone) - user.offset).date()
        if user.last_sent == today:
            return

        ### send a message
        try:
            message = await self.prepare_message(user)
            await after.send(message)
        except:
            logging.exception("Failed to send a message")
            raise

        ### record that the message was sent
        user.last_sent = today

        target = weather_dir / f"{after.id}.json"
        backup = weather_dir / f"{after.id}.backup.json"

        target.rename(backup)
        with open(target, "w") as file:
            file.write(user.model_dump_json(indent=self.mconfig.indent))
