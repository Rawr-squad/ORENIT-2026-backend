from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.models import Module, Achievement
from app.core.db import get_db
from app.core.dependencies import require_role
from app.schemas.module import ModuleCreate

router = APIRouter(prefix="/admin/achievements")


@router.post("")
def create_achievement(
    title: str,
    description: str,
    type: str,
    condition_value: int,
    reward_coins: int,
    db: Session = Depends(get_db),
    admin=Depends(require_role(["admin"]))
):
    ach = Achievement(
        title=title,
        description=description,
        type=type,
        condition_value=condition_value,
        reward_coins=reward_coins
    )
    db.add(ach)
    db.commit()
    return ach