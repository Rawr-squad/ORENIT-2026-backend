from pydantic import BaseModel, constr
from typing import Optional, List
from datetime import datetime


class CommentCreate(BaseModel):
    lesson_id: int
    content: constr(min_length=1, max_length=1000)
    parent_id: Optional[int] = None


class CommentResponse(BaseModel):
    id: int
    user_id: int
    nickname: str
    content: str
    created_at: datetime
    replies: List["CommentResponse"] = []

    class Config:
        from_attributes = True