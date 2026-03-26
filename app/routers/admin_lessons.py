from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Lesson
from app.core.db import get_db
from app.core.dependencies import require_role
from app.schemas.lesson import LessonCreate

router = APIRouter(prefix="/admin/lessons")


@router.post("")
def create_lesson(
    data: LessonCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_role(["admin"]))
):
    lesson = Lesson(**data.model_dump())
    db.add(lesson)
    db.commit()
    return lesson