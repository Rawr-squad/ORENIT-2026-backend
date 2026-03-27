from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CommentCreate(BaseModel):
    lesson_id: int = Field(gt=0)
    content: str = Field(min_length=1, max_length=1000)
    parent_id: Optional[int] = Field(default=None, gt=0)


class CommentResponse(BaseModel):
    id: int
    user_id: int
    nickname: str
    content: str
    created_at: datetime
    replies: List["CommentResponse"] = []

    class Config:
        from_attributes = True