from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.models import Progress, Currency, ParentChild, User, UserAchievement
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

    lesson = ProgressService(db).start_lesson(user.id, data.lesson_id)
    db.refresh(lesson)

    return lesson


@router.get("/me")
def my_progress(user=Depends(get_current_user), db: Session = Depends(get_db)):

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
        "nickname_color": target_user.nickname_color,
        "status": target_user.status_title,
        "xp": xp.xp if xp else 0,
        "coins" : xp.coins if xp else 0,
        **stats
    }


from sqlalchemy import func


@router.get("/leaderboard")
def leaderboard(db: Session = Depends(get_db)):
    results = (
        db.query(
            User,
            Currency.xp,
            Currency.coins,
            func.count(UserAchievement.user_id).label("achievements_count")
        )
        .join(Currency, User.id == Currency.user_id)
        .outerjoin(UserAchievement, UserAchievement.user_id == User.id)
        .group_by(User.id, Currency.xp, Currency.coins)
        .order_by(Currency.xp.desc())
        .limit(10)
        .all()
    )

    return [
        {
            "user_id": user.id,
            "nickname": user.nickname,
            "nickname_color" : user.nickname_color,
            "status_title" : user.status_title,
            "xp": xp,
            "coins": coins,
            "achievements_count": achievements_count,
        }
        for user, xp, coins, achievements_count in results
    ]