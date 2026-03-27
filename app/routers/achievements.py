from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.models import Achievement, UserAchievement
from app.core.dependencies import get_current_user

router = APIRouter(prefix="/achievements", tags=["achievements"])


@router.get("")
def get_all(db: Session = Depends(get_db)):
    return db.query(Achievement).all()


@router.get("/me")
def my_achievements(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(UserAchievement).filter_by(user_id=user.id).all()


@router.get("/{id}")
def get_one(id: int, db: Session = Depends(get_db)):
    ach = db.get(Achievement, id)
    if not ach:
        raise Exception("Not found")
    return ach

@router.post('/once')
def get_all(db=Depends(get_db)):
    achievements = [
        ("First Steps", "Solve 3 tasks", "tasks_completed", 3, 10),
        ("Getting Better", "Solve 5 tasks", "tasks_completed", 5, 20),
        ("Pro Solver", "Solve 10 tasks", "tasks_completed", 10, 50),

        ("Starter", "Complete 3 lessons", "lessons_completed", 3, 30),
        ("Advanced", "Complete 5 lessons", "lessons_completed", 5, 60),
    ]

    for title, desc, type_, cond, reward in achievements:
        db.add(Achievement(
            title=title,
            description=desc,
            type=type_,
            condition_value=cond,
            reward_coins=reward
        ))
    db.commit()
    return "ok"

