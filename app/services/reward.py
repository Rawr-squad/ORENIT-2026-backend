from datetime import datetime, date
from fastapi import HTTPException

from app.models.models import User, Currency


class RewardService:

    def __init__(self, db):
        self.db = db

    def claim_daily_reward(self, user_id: int):
        user = self.db.get(User, user_id)

        if not user:
            raise HTTPException(404, "User not found")

        today = date.today()

        if user.last_reward_at and user.last_reward_at.date() == today:
            raise HTTPException(400, "Reward already claimed today")

        currency = self.db.get(Currency, user_id)
        if not currency:
            currency = Currency(user_id=user_id, xp=0, coins=0)
            self.db.add(currency)

        coins_reward = 15
        xp_reward = 50

        currency.coins += coins_reward
        currency.xp += xp_reward

        user.last_reward_at = datetime.utcnow()

        self.db.commit()

        return {
            "coins": coins_reward,
            "xp": xp_reward,
            "message": "Daily reward claimed"
        }