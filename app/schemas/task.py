from pydantic import BaseModel, Field
from typing import Optional, Literal


class TaskCreate(BaseModel):
    lesson_id: int = Field(gt=0)
    type: Literal["quiz", "input", "code"]
    question: str = Field(min_length=5, max_length=2000)
    correct_answer: Optional[str] = Field(default=None, max_length=2000)
    coins: int = Field(ge=0, le=100)


class TaskSubmit(BaseModel):
    answer: str = Field(min_length=1, max_length=5000)