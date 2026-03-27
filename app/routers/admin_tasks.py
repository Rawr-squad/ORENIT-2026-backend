from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.models import Task
from app.core.db import get_db
from app.core.dependencies import require_role
from app.schemas.task import TaskCreate

router = APIRouter(prefix="/admin/tasks")


@router.post("")
def create_task(data: TaskCreate, db=Depends(get_db), admin=Depends(require_role(["admin"]))):

    exists = db.query(Task).filter_by(lesson_id=data.lesson_id).first()

    if exists:
        raise HTTPException(400, "Only one task allowed per lesson")

    task = Task(**data.model_dump())
    db.add(task)
    db.commit()
    return task


@router.put("/{id}")
def update_task(id: int, data: TaskCreate, db=Depends(get_db), admin=Depends(require_role(["admin"]))):
    task = db.get(Task, id)

    if not task:
        raise HTTPException(404, "Task not found")

    for k, v in data.model_dump().items():
        setattr(task, k, v)

    db.commit()
    return task


@router.delete("/{id}")
def delete_task(id: int, db=Depends(get_db), admin=Depends(require_role(["admin"]))):
    task = db.get(Task, id)

    if not task:
        raise HTTPException(404, "Task not found")

    db.delete(task)
    db.commit()

    return {"message": "Task deleted"}