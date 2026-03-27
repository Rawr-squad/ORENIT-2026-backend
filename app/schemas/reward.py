from pydantic import BaseModel, Field


class DailyRewardResponse(BaseModel):
    coins: int = Field(ge=0)
    xp: int = Field(ge=0)
    message: str