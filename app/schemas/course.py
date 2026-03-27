from pydantic import BaseModel, Field


class CourseCreate(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=10, max_length=2000)


class CourseResponse(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True