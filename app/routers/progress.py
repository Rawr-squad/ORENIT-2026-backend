from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.models import Progress, Currency
from app.core.dependencies import get_current_user
from app.schemas.progress import StartLessonRequest
from app.services.progress import ProgressService

router = APIRouter(prefix="/progress")


@router.post("/start")
def start_lesson(
    data: StartLessonRequest,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):


    return ProgressService(db).start_lesson(user.id, data.lesson_id)


@router.get("/me")
def my_progress(user=Depends(get_current_user), db: Session = Depends(get_db)):
    service = ProgressService(db)

    stats = service.get_progress(user.id)

    xp = db.get(Currency, user.id)

    return {
        "xp": xp.xp if xp else 0,
        **stats
    }


@router.get("/leaderboard")
def leaderboard(db: Session = Depends(get_db)):
    return db.query(Currency).order_by(Currency.xp.desc()).limit(10).all()