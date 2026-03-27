from pydantic import BaseModel
from typing import Optional, Literal

class TaskCreate(BaseModel):
    lesson_id: int
    type: Literal["quiz", "input", "code"]
    question: str
    correct_answer: Optional[str]
    coins : int


class TaskSubmit(BaseModel):
    answer: str