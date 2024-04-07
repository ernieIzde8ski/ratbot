from typing import Annotated

from owmpy.utils import StandardUnits  # type: ignore
from owmpy.utils import Units as BaseUnits  # type: ignore
from pydantic import PlainSerializer, PlainValidator, ValidationError


def _validate_units(value: str) -> BaseUnits:
    value = value.upper()
    match value:
        case "IMPERIAL" | "METRIC" | "STANDARD":
            return getattr(StandardUnits, value)
        case default:
            raise ValidationError(f"Unrecognized units: '{value}'")


def _serialize_units(units: BaseUnits) -> str:
    match units:
        case StandardUnits.IMPERIAL:
            return "IMPERIAL"
        case StandardUnits.METRIC:
            return "METRIC"
        case StandardUnits.STANDARD:
            return "STANDARD"
        case default:
            raise ValidationError("Unrecognized units")


Units = Annotated[
    BaseUnits,
    PlainValidator(_validate_units),
    PlainSerializer(_serialize_units, return_type=str),
]
