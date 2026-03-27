from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.schemas.task import TaskSubmit
from app.services.task import TaskService
from app.core.db import get_db

router = APIRouter()


@router.post("/tasks/{task_id}/submit")
def submit(
    task_id: int,
    data: TaskSubmit,
    user=Depends(get_current_user),
    db=Depends(get_db)
):
    task = TaskService(db).submit(user, task_id, data.answer)
    db.refresh(task)

    return task