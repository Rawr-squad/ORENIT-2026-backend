from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.models import Progress, Currency
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/progress")


@router.get("/me")
def my_progress(user=Depends(get_current_user), db: Session = Depends(get_db)):
    xp = db.get(Currency, user.id)
    lessons = db.query(Progress).filter_by(user_id=user.id, completed=True).count()

    return {
        "xp": xp.xp if xp else 0,
        "completed_lessons": lessons
    }


@router.get("/leaderboard")
def leaderboard(db: Session = Depends(get_db)):
    return db.query(Currency).order_by(Currency.xp.desc()).limit(10).all()