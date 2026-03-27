from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.schemas.comment import CommentCreate
from app.services.comment import CommentService

router = APIRouter(prefix="/comments", tags=["comments"])


@router.post("")
def create_comment(
    data: CommentCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    comment = CommentService(db).create_comment(user, data)
    db.refresh(comment)
    return comment


@router.get("/lesson/{lesson_id}")
def get_comments(lesson_id: int, db: Session = Depends(get_db)):

    comment = CommentService(db).get_comments_tree(lesson_id)

    return comment