from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import Lesson
from app.core.db import get_db
from app.core.dependencies import require_role
from app.schemas.lesson import LessonCreate

router = APIRouter(prefix="/admin/lessons")


@router.post("")
def create_lesson(data: LessonCreate, db=Depends(get_db), admin=Depends(require_role(["admin"]))):

    exists = db.query(Lesson).filter(
        Lesson.module_id == data.module_id,
        Lesson.order == data.order
    ).first()

    if exists:
        raise HTTPException(400, "Lesson order already exists in module")

    lesson = Lesson(**data.model_dump())
    db.add(lesson)
    db.commit()
    return lesson


@router.put("/{id}")
def update_lesson(id: int, data: LessonCreate, db=Depends(get_db), admin=Depends(require_role(["admin"]))):

    lesson = db.get(Lesson, id)
    if not lesson:
        raise HTTPException(404, "Lesson not found")

    exists = db.query(Lesson).filter(
        Lesson.module_id == data.module_id,
        Lesson.order == data.order,
        Lesson.id != id
    ).first()

    if exists:
        raise HTTPException(400, "Lesson order conflict")

    for k, v in data.model_dump().items():
        setattr(lesson, k, v)

    db.commit()
    return lesson


@router.delete("/{id}")
def delete_lesson(id: int, db=Depends(get_db), admin=Depends(require_role(["admin"]))):
    lesson = db.get(Lesson, id)

    if not lesson:
        raise HTTPException(404, "Lesson not found")

    db.delete(lesson)
    db.commit()

    return {"message": "Lesson deleted"}