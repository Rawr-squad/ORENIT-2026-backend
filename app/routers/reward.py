from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.core.dependencies import get_current_user
from app.services.reward import RewardService
from app.schemas.reward import DailyRewardResponse

router = APIRouter(prefix="/reward", tags=["reward"])


@router.post("/daily", response_model=DailyRewardResponse)
def daily_reward(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):

    return RewardService(db).claim_daily_reward(user.id)