from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, Enum
from datetime import datetime
import enum
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


class AttemptStatus(str, enum.Enum):
    pending = "pending"
    checked = "checked"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    password_hash = Column(String)
    role = Column(Enum(Role))
    created_at = Column(DateTime, default=datetime.utcnow)


class ParentChild(Base):
    __tablename__ = "parent_child"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("users.id"))
    child_id = Column(Integer, ForeignKey("users.id"))


class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(Text)


class Module(Base):
    __tablename__ = "modules"
    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    title = Column(String)
    order = Column(Integer)


class Lesson(Base):
    __tablename__ = "lessons"
    id = Column(Integer, primary_key=True)
    module_id = Column(Integer, ForeignKey("modules.id"))
    title = Column(String)
    theory_content = Column(Text)
    order = Column(Integer)


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    type = Column(Enum(TaskType))
    question = Column(Text)
    correct_answer = Column(Text, nullable=True)
    order = Column(Integer)


class Attempt(Base):
    __tablename__ = "attempts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    task_id = Column(Integer, ForeignKey("tasks.id"))
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
    lesson_id = Column(Integer, ForeignKey("lessons.id"))
    status = Column(Enum(ProgressStatus), default=ProgressStatus.started)

class Currency(Base):
    __tablename__ = "currency"
    user_id = Column(Integer, primary_key=True)
    xp = Column(Integer, default=0)
    coins = Column(Integer, default=0)