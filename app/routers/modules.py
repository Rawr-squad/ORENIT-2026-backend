from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, load_only
from app.core.db import get_db
from app.models.models import Module, Lesson

router = APIRouter(prefix="/modules")


@router.get("")
def get_modules(db: Session = Depends(get_db)):
    return db.query(Module).all()


@router.get("/{id}")
def get_course(id: int, db: Session = Depends(get_db)):
    module = db.get(Module, id)
    if not module:
        raise HTTPException(404, "Module not found")

    lessons = db.query(Lesson).filter_by(module_id=module.id).options(
        load_only(Lesson.id, Lesson.title, Lesson.order)
    ).all()

    return {"id": module.id, "title": module.title, "lessons": lessons}