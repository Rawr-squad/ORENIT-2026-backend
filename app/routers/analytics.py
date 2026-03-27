from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.services.analytics import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


@router.get("/weak-lessons")
def weak_lessons(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return AnalyticsService(db).get_weak_lessons(user.id)