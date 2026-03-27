from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, load_only
from app.core.db import get_db
from app.models.models import Lesson, Task

router = APIRouter(prefix="/lessons")


@router.get("/{id}")
def get_lesson(id: int, db: Session = Depends(get_db)):
    lesson = db.get(Lesson, id)
    if not lesson:
        raise HTTPException(404, "Lesson not found")

    tasks = db.query(Task).filter_by(lesson_id=lesson.id).options(
        load_only(Task.id, Task.type, Task.question, Task.coins)
    ).all()

    return {"id": lesson.id, "title": lesson.title,
            "theory_content": lesson.theory_content,
            "order": lesson.order, "tasks": tasks}