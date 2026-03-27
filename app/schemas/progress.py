from pydantic import BaseModel, Field


class StartLessonRequest(BaseModel):
    lesson_id: int = Field(gt=0)