from fastapi import APIRouter, Depends
from app.core.dependencies import get_current_user
from app.services.task import TaskService
from app.core.db import get_db

router = APIRouter()


@router.post("/tasks/{task_id}/submit")
def submit(task_id: int, answer: str, user=Depends(get_current_user), db=Depends(get_db)):
    return TaskService(db).submit(user, task_id, answer)