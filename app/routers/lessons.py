from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.models import Lesson

router = APIRouter(prefix="/lessons")


@router.get("/{id}")
def get_lesson(id: int, db: Session = Depends(get_db)):
    return db.get(Lesson, id)