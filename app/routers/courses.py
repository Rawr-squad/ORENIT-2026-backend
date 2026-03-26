from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.models import Course

router = APIRouter(prefix="/courses")


@router.get("")
def get_courses(db: Session = Depends(get_db)):
    return db.query(Course).all()


@router.get("/{id}")
def get_course(id: int, db: Session = Depends(get_db)):
    return db.get(Course, id)