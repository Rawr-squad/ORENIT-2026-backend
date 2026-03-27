from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.models import Progress, Lesson, Task, Attempt, ProgressStatus, AttemptStatus, TaskType


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

    def check_lesson_completed(self, user_id: int, lesson_id: int):
        tasks = self.db.query(Task).filter_by(lesson_id=lesson_id).all()

        if not tasks:
            return False

        for task in tasks:

            if task.type in [TaskType.quiz, TaskType.input]:
                attempt = self.db.query(Attempt).filter(
                    Attempt.user_id == user_id,
                    Attempt.task_id == task.id,
                    Attempt.is_correct == True
                ).first()

                if not attempt:
                    return False

            elif task.type == TaskType.code:
                attempt = self.db.query(Attempt).filter(
                    Attempt.user_id == user_id,
                    Attempt.task_id == task.id,
                    Attempt.status == AttemptStatus.checked,
                    Attempt.is_correct == True
                ).first()

                if not attempt:
                    return False

        # 🔥 если дошли сюда — все задачи выполнены
        progress = self.db.query(Progress).filter_by(
            user_id=user_id,
            lesson_id=lesson_id
        ).first()

        if not progress:
            raise HTTPException(400, "Lesson not started")

        if progress.status != ProgressStatus.completed:
            progress.status = ProgressStatus.completed
            self.db.commit()

            from app.services.achievement import AchievementService
            AchievementService(self.db).check_achievements(user_id)

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