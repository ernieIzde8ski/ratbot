from typing import Annotated
from zoneinfo import ZoneInfo as BaseZoneInfo

from pydantic import PlainSerializer, PlainValidator

ZoneInfo = Annotated[
    BaseZoneInfo,
    PlainValidator(BaseZoneInfo),
    PlainSerializer(lambda z: z.key, return_type=str),
]
