from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, load_only
from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.models.models import Lesson, Task, Progress

router = APIRouter(prefix="/lessons")


@router.get("/{id}")
def get_lesson(
        id: int,
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    lesson = db.get(Lesson, id)
    if not lesson:
        raise HTTPException(404, "Lesson not found")

    # Получаем статус урока для текущего пользователя
    progress = db.query(Progress).filter_by(
        user_id=current_user.id,
        lesson_id=lesson.id
    ).first()

    lesson_status = progress.status if progress else "not_started"

    tasks = db.query(Task).filter_by(lesson_id=lesson.id).options(
        load_only(Task.id, Task.type, Task.question, Task.coins)
    ).all()

    return {
        "id": lesson.id,
        "title": lesson.title,
        "theory_content": lesson.theory_content,
        "order": lesson.order,
        "status": lesson_status,
        "tasks": tasks
    }