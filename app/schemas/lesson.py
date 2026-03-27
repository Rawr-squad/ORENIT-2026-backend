from pydantic import BaseModel, Field


class LessonCreate(BaseModel):
    module_id: int = Field(gt=0)
    title: str = Field(min_length=3, max_length=100)
    theory_content: str = Field(min_length=5, max_length=10000)
    order: int = Field(ge=0)