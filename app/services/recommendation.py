from sqlalchemy.orm import Session
from app.models.models import Lesson, Progress, ProgressStatus, Module


class RecommendationService:

    def __init__(self, db: Session):
        self.db = db

    def get_next_lesson(self, user_id: int):
        # все уроки с сортировкой
        lessons = (
            self.db.query(Lesson)
            .join(Module, Lesson.module_id == Module.id)
            .order_by(Module.order.asc(), Lesson.order.asc())
            .all()
        )

        # прогресс пользователя
        completed_ids = {
            p.lesson_id
            for p in self.db.query(Progress).filter_by(
                user_id=user_id,
                status=ProgressStatus.completed
            ).all()
        }

        for lesson in lessons:
            if lesson.id not in completed_ids:
                return lesson

        return None