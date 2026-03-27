from sqlalchemy.orm import Session
from app.models.models import Progress, Lesson, Task, Attempt, ProgressStatus


class ProgressService:

    def __init__(self, db: Session):
        self.db = db

    # 🚀 старт урока
    def start_lesson(self, user_id: int, lesson_id: int):
        existing = self.db.query(Progress).filter_by(
            user_id=user_id,
            lesson_id=lesson_id
        ).first()

        if existing:
            raise Exception("Lesson already started")

        progress = Progress(
            user_id=user_id,
            lesson_id=lesson_id,
            status=ProgressStatus.started
        )

        self.db.add(progress)
        self.db.commit()
        return progress

    # ✅ проверка завершения урока
    def check_lesson_completed(self, user_id: int, lesson_id: int):
        tasks = self.db.query(Task).filter_by(lesson_id=lesson_id).all()

        for task in tasks:
            attempt = self.db.query(Attempt).filter_by(
                user_id=user_id,
                task_id=task.id,
                is_correct=True
            ).first()

            if not attempt:
                return False

        progress = self.db.query(Progress).filter_by(
            user_id=user_id,
            lesson_id=lesson_id
        ).first()

        if progress:
            progress.status = ProgressStatus.completed
            self.db.commit()

        return True

    # 📊 агрегированный прогресс
    def get_progress(self, user_id: int):
        total_lessons = self.db.query(Lesson).count()

        started = self.db.query(Progress).filter_by(
            user_id=user_id,
            status=ProgressStatus.started
        ).count()

        completed = self.db.query(Progress).filter_by(
            user_id=user_id,
            status=ProgressStatus.completed
        ).count()

        not_started = total_lessons - (started + completed)

        return {
            "started_lessons": started,
            "completed_lessons": completed,
            "not_started_lessons": not_started,
        }