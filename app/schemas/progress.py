from pydantic import BaseModel

class StartLessonRequest(BaseModel):
    lesson_id: int