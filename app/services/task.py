from app.models.models import Attempt, Task


class TaskService:
    def __init__(self, db):
        self.db = db

    def submit(self, user, task_id, answer):
        task = self.db.get(Task, task_id)

        if task.type in ["quiz", "input"]:
            correct = answer == task.correct_answer

            attempt = Attempt(
                user_id=user.id,
                task_id=task_id,
                answer=answer,
                is_correct=correct,
                status="checked",
            )

            self.db.add(attempt)

            if correct:
                self._add_xp(user.id, 10)

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