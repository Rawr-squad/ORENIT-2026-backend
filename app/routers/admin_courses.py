from fastapi import APIRouter, Depends
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
    course = Course(**data.model_dump())
    db.add(course)
    db.commit()
    return course


@router.put("/{id}")
def update_course(
    id: int,
    data: CourseCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_role(["admin"]))
):
    course = db.get(Course, id)
    for k, v in data.model_dump().items():
        setattr(course, k, v)

    db.commit()
    return course