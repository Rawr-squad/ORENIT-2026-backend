from pydantic import BaseModel

class ModuleCreate(BaseModel):
    course_id: int
    title: str
    order: int

class ModuleResponse(BaseModel):
    id: int
    course_id: int
    title: str
    order: int

    class Config:
        from_attributes = True