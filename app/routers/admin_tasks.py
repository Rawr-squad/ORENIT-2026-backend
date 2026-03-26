from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Task
from app.core.db import get_db
from app.core.dependencies import require_role
from app.schemas.task import TaskCreate

router = APIRouter(prefix="/admin/tasks")


@router.post("")
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_role(["admin"]))
):
    task = Task(**data.model_dump())
    db.add(task)
    db.commit()
    return task