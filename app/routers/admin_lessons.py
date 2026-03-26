from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Lesson
from app.core.db import get_db
from app.core.dependencies import require_role

router = APIRouter(prefix="/admin/lessons")


@router.post("")
def create_lesson(module_id: int, title: str, theory_content: str, order: int,
                  db: Session = Depends(get_db),
                  admin=Depends(require_role(["admin"]))):
    lesson = Lesson(
        module_id=module_id,
        title=title,
        theory_content=theory_content,
        order=order
    )
    db.add(lesson)
    db.commit()
    return lesson