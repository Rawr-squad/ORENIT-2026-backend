from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Task
from app.core.db import get_db
from app.core.dependencies import require_role

router = APIRouter(prefix="/admin/tasks")


@router.post("")
def create_task(
    lesson_id: int,
    type: str,
    question: str,
    correct_answer: str | None,
    order: int,
    db: Session = Depends(get_db),
    admin=Depends(require_role(["admin"]))
):
    task = Task(
        lesson_id=lesson_id,
        type=type,
        question=question,
        correct_answer=correct_answer,
        order=order
    )
    db.add(task)
    db.commit()
    return task