from pydantic import BaseModel, Field
from typing import Optional, Literal


from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from typing import Literal


class TaskCreate(BaseModel):
    lesson_id: int = Field(gt=0)
    type: Literal["quiz", "input", "code"]
    question: str = Field(min_length=5, max_length=2000)
    correct_answer: Optional[str] = Field(default=None, max_length=2000)
    coins: int = Field(ge=0, le=100)

    options: Optional[List[str]] = None

    @field_validator("options")
    @classmethod
    def validate_options(cls, v):
        if v is None:
            return v

        if not isinstance(v, list):
            raise ValueError("Options must be a list")

        if len(v) < 2:
            raise ValueError("At least 2 options required")

        for opt in v:
            if not isinstance(opt, str) or not opt.strip():
                raise ValueError("Invalid option")

        return v

    @field_validator("correct_answer")
    @classmethod
    def validate_correct_answer(cls, v, values):
        task_type = values.data.get("type")

        if task_type == "quiz":
            if not v:
                raise ValueError("Quiz must have correct_answer")

        return v

class TaskSubmit(BaseModel):
    answer: str = Field(min_length=1, max_length=5000)