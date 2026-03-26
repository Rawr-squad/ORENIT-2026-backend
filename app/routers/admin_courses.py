from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.dependencies import require_role
from app.models.models import Course

router = APIRouter(prefix="/admin/courses", tags=["admin"])


@router.post("")
def create_course(
    title: str,
    description: str,
    db: Session = Depends(get_db),
    admin=Depends(require_role(["admin"]))
):
    course = Course(title=title, description=description)
    db.add(course)
    db.commit()
    return course


@router.put("/{id}")
def update_course(id: int, title: str, description: str, db=Depends(get_db), admin=Depends(require_role(["admin"]))):
    course = db.get(Course, id)
    course.title = title
    course.description = description
    db.commit()
    return course


@router.delete("/{id}")
def delete_course(id: int, db=Depends(get_db), admin=Depends(require_role(["admin"]))):
    course = db.get(Course, id)
    db.delete(course)
    db.commit()
    return {"ok": True}