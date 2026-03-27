from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.models import Progress, Currency, ParentChild, User
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

    # 👇 если родитель → берём ребёнка
    if user.role == "parent":
        link = db.query(ParentChild).filter_by(parent_id=user.id).first()

        if not link:
            raise HTTPException(404, "No child linked")

        target_user_id = link.child_id
        target_user = db.get(User, target_user_id)

    else:
        target_user_id = user.id
        target_user = user

    service = ProgressService(db)
    stats = service.get_progress(target_user_id)

    xp = db.get(Currency, target_user_id)

    return {
        "user_id": target_user_id,
        "nickname": target_user.nickname,
        "xp": xp.xp if xp else 0,
        "coins" : xp.coins if xp else 0
        **stats
    }


@router.get("/leaderboard")
def leaderboard(db: Session = Depends(get_db)):

    results = db.query(Currency, User).join(
        User, User.id == Currency.user_id
    ).order_by(Currency.xp.desc()).limit(10).all()

    return [
        {
            "user_id": user.id,
            "nickname": user.nickname,
            "xp": currency.xp
        }
        for currency, user in results
    ]