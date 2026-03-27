from app.models.models import (
    Achievement,
    UserAchievement,
    Attempt,
    Progress,
    Currency,
    AchievementType,
)


class AchievementService:

    def __init__(self, db):
        self.db = db

    def check_achievements(self, user_id: int):
        achievements = self.db.query(Achievement).all()

        for ach in achievements:

            already = self.db.query(UserAchievement).filter_by(
                user_id=user_id,
                achievement_id=ach.id
            ).first()

            if already:
                continue

            if self._check_condition(user_id, ach):
                self._grant(user_id, ach)

    def _check_condition(self, user_id, ach: Achievement):

        if ach.type == AchievementType.tasks_completed:
            count = self.db.query(Attempt).filter_by(
                user_id=user_id,
                is_correct=True
            ).count()

            return count >= ach.condition_value

        if ach.type == AchievementType.lessons_completed:
            count = self.db.query(Progress).filter_by(
                user_id=user_id,
                status="completed"
            ).count()

            return count >= ach.condition_value

        return False

    def _grant(self, user_id, ach: Achievement):
        ua = UserAchievement(
            user_id=user_id,
            achievement_id=ach.id
        )

        self.db.add(ua)

        currency = self.db.get(Currency, user_id)
        if not currency:
            currency = Currency(user_id=user_id, xp=0, coins=0)
            self.db.add(currency)

        currency.coins += ach.reward_coins

        self.db.commit()