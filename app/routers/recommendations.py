from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.services.recommendation import RecommendationService

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/next")
def get_next_lesson(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    lesson = RecommendationService(db).get_next_lesson(user.id)

    if not lesson:
        raise HTTPException(404, "No lessons left")

    return {
        "lesson_id": lesson.id,
        "title": lesson.title,
        "module_id": lesson.module_id
    }