from pydantic import BaseModel, Field


class ModuleCreate(BaseModel):
    course_id: int = Field(gt=0)
    title: str = Field(min_length=3, max_length=100)
    order: int = Field(ge=0)


class ModuleResponse(BaseModel):
    id: int
    course_id: int
    title: str
    order: int

    class Config:
        from_attributes = True