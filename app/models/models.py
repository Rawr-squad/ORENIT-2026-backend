from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, Enum, func
from datetime import datetime
import enum

from sqlalchemy.orm import relationship

from app.core.db import Base


class Role(str, enum.Enum):
    student = "student"
    parent = "parent"
    admin = "admin"

class ProgressStatus(str, enum.Enum):
    started = "started"
    completed = "completed"

class TaskType(str, enum.Enum):
    quiz = "quiz"
    input = "input"
    code = "code"

class AchievementType(str, enum.Enum):
    tasks_completed = "tasks_completed"
    lessons_completed = "lessons_completed"

class AttemptStatus(str, enum.Enum):
    pending = "pending"
    checked = "checked"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    nickname = Column(String, nullable=False)
    email = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(Enum(Role))
    nickname_color = Column(String, nullable=True)  # HEX
    status_title = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_reward_at = Column(DateTime, nullable=True)

class NicknameColor(Base):
    __tablename__ = "nickname_colors"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    hex_code = Column(String)  # #FF0000
    price = Column(Integer)

class UserStatus(Base):
    __tablename__ = "user_statuses"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    price = Column(Integer)


class ParentChild(Base):
    __tablename__ = "parent_child"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("users.id"))
    child_id = Column(Integer, ForeignKey("users.id"))

class Achievement(Base):
    __tablename__ = "achievements"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    description = Column(String)

    type = Column(Enum(AchievementType))
    condition_value = Column(Integer)  # например 3, 5, 10

    reward_coins = Column(Integer)

class UserAchievement(Base):
    __tablename__ = "user_achievements"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    achievement_id = Column(Integer, ForeignKey("achievements.id"), primary_key=True)


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)


class Module(Base):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True)
    Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"))
    title = Column(String)
    order = Column(Integer)


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id", ondelete="CASCADE"))
    title = Column(String)
    theory_content = Column(Text)
    order = Column(Integer)

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"))

    parent_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"))

    content = Column(String, nullable=False)

    created_at = Column(DateTime, server_default=func.now())

    # связи (опционально)
    parent = relationship("Comment", remote_side=[id])


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"))
    type = Column(Enum(TaskType))
    question = Column(Text)
    correct_answer = Column(Text, nullable=True)
    coins = Column(Integer, default=0)


class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"))
    answer = Column(Text)
    is_correct = Column(Boolean, nullable=True)
    status = Column(Enum(AttemptStatus))
    reviewer_id = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)


class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(Integer, ForeignKey("lessons.id", ondelete="CASCADE"))
    status = Column(Enum(ProgressStatus), default=ProgressStatus.started)

class Currency(Base):
    __tablename__ = "currency"
    user_id = Column(Integer, primary_key=True)
    xp = Column(Integer, default=0)
    coins = Column(Integer, default=0)