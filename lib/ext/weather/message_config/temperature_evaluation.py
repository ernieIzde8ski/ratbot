from pydantic import BaseModel


class TemperatureEvaluation(BaseModel):
    threshold: int | float
    """Highest temperature that merits this evaluation."""
    message: str | list[str]
    """Message to accompany this evaluation."""
