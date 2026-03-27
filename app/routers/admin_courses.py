from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.core.dependencies import require_role
from app.models.models import Course
from app.schemas.course import CourseCreate

router = APIRouter(prefix="/admin/courses", tags=["admin"])


@router.post("")
def create_course(
    data: CourseCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_role(["admin"]))
):
    existing = db.query(Course).filter_by(title=data.title).first()
    if existing:
        raise HTTPException(400, "Course already exists")

    course = Course(**data.model_dump())
    db.add(course)
    db.commit()
    return course


@router.put("/{id}")
def update_course(id: int, data: CourseCreate, db=Depends(get_db), admin=Depends(require_role(["admin"]))):
    course = db.get(Course, id)

    if not course:
        raise HTTPException(404, "Course not found")

    exists = db.query(Course).filter(Course.title == data.title, Course.id != id).first()
    if exists:
        raise HTTPException(400, "Course with this title already exists")

    course.title = data.title
    course.description = data.description

    db.commit()
    return course


@router.delete("/{id}")
def delete_course(id: int, db=Depends(get_db), admin=Depends(require_role(["admin"]))):
    course = db.get(Course, id)

    if not course:
        raise HTTPException(404, "Course not found")

    db.delete(course)
    db.commit()

    return {"message": "Course deleted"}