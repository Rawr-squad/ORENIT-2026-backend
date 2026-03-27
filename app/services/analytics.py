from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.models import Attempt, Lesson, Task


class AnalyticsService:

    def __init__(self, db: Session):
        self.db = db

    def get_weak_lessons(self, user_id: int, limit: int = 3):
        # считаем ошибки по урокам
        results = (
            self.db.query(
                Task.lesson_id,
                func.count(Attempt.id).label("errors")
            )
            .join(Task, Task.id == Attempt.task_id)
            .filter(
                Attempt.user_id == user_id,
                Attempt.is_correct == False
            )
            .group_by(Task.lesson_id)
            .order_by(func.count(Attempt.id).desc())
            .limit(limit)
            .all()
        )

        lesson_ids = [r.lesson_id for r in results]

        lessons = self.db.query(Lesson).filter(Lesson.id.in_(lesson_ids)).all()

        lesson_map = {l.id: l for l in lessons}

        return [
            {
                "lesson_id": r.lesson_id,
                "title": lesson_map[r.lesson_id].title if r.lesson_id in lesson_map else None,
                "errors": r.errors
            }
            for r in results
        ]