import logging
import random
from pathlib import Path
from typing import Self

from pydantic import BaseModel
from yaml import safe_load

from lib import dirs

from .temperature_evaluation import TemperatureEvaluation


class MessageConfig(BaseModel):
    greeting: list[str]
    morning_greeting: list[str]
    min_quotes: int
    max_quotes: int
    temp_evals: list[TemperatureEvaluation]
    default_eval: str
    indent: int | None = None

    @classmethod
    def load_or_default(cls) -> Self:
        path = dirs.weather_home() / "message_config.yaml"

        if path.exists():
            data = safe_load(path.read_text())
        else:
            default_path = Path(__file__).parent / "message_config_default.yaml"
            logging.warning("Weather configuration file does not exist.")
            logging.warning(
                "You can suppress this warning by copying the default configuration:"
            )
            logging.warning(f"\t$ cp '{default_path}' '{path}'")
            data = safe_load(default_path.read_text())

        resp = cls.model_validate(data)
        resp.temp_evals.sort(key=lambda te: te.threshold)
        return resp

    def evaluate_temperature(self, temp: int | float) -> str:
        for eval in self.temp_evals:
            if temp < eval.threshold:
                if isinstance(eval.message, list):
                    return random.choice(eval.message)
                else:
                    return eval.message
        return self.default_eval
