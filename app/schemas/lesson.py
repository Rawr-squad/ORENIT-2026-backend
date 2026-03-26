from pydantic import BaseModel

class LessonCreate(BaseModel):
    module_id: int
    title: str
    theory_content: str
    order: int