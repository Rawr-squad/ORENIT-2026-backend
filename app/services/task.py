from fastapi import HTTPException

from app.models.models import Attempt, Task, Currency
from app.services.achievement import AchievementService
from app.services.progress import ProgressService


class TaskService:
    def __init__(self, db):
        self.db = db

    def submit(self, user, task_id, answer):
        task = self.db.get(Task, task_id)

        if not task:
            raise HTTPException(404, "Task not found")

        existing_attempt = self.db.query(Attempt).filter(
            Attempt.user_id == user.id,
            Attempt.task_id == task_id,
            Attempt.is_correct == True  # Только успешные попытки
        ).first()

        if existing_attempt:
            raise HTTPException(400, "Task already completed")

        if task.type in ["quiz", "input"]:
            is_correct = answer == task.correct_answer

            currency = self.db.get(Currency, user.id)
            if not currency:
                currency = Currency(user_id=user.id, xp=0, coins=0)
                self.db.add(currency)

            task.coins = task.coins if task.coins is not None else 0

            if is_correct:
                currency.coins += task.coins

            attempt = Attempt(
                user_id=user.id,
                task_id=task_id,
                answer=answer,
                is_correct=is_correct,
                status="checked"
            )

            self.db.add(attempt)

            if is_correct:
                self._add_xp(user.id, 10)

            self.db.commit()

            ProgressService(self.db).check_lesson_completed(
                user.id,
                task.lesson_id
            )

            AchievementService(self.db).check_achievements(user.id)
            return attempt

        else:
            attempt = Attempt(
                user_id=user.id,
                task_id=task_id,
                answer=answer,
                status="pending",
            )
            self.db.add(attempt)
            self.db.commit()
            return attempt

    def _add_xp(self, user_id, xp):
        from app.models.models import Currency

        cur = self.db.get(Currency, user_id)
        if not cur:
            cur = Currency(user_id=user_id, xp=0)
            self.db.add(cur)

        cur.xp += xp