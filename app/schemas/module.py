from pydantic import BaseModel

class ModuleCreate(BaseModel):
    course_id: int
    title: str
    order: int