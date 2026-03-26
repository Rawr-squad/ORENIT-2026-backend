from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Module
from app.core.db import get_db
from app.core.dependencies import require_role

router = APIRouter(prefix="/admin/modules")


@router.post("")
def create_module(course_id: int, title: str, order: int, db: Session = Depends(get_db), admin=Depends(require_role(["admin"]))):
    m = Module(course_id=course_id, title=title, order=order)
    db.add(m)
    db.commit()
    return m