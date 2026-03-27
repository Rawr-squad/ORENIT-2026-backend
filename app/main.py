from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.db import Base, engine
from app.routers import auth, courses, lessons, tasks, parent_child, \
    admin_courses, admin_modules, admin_lessons, admin_tasks, \
    admin_attempts, progress, admin_achievements, achievements, \
    shop, admin_shop

app = FastAPI(title="Edu Platform")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# routers
app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(lessons.router)
app.include_router(tasks.router)
app.include_router(parent_child.router)
app.include_router(progress.router)
app.include_router(admin_courses.router)
app.include_router(admin_modules.router)
app.include_router(admin_lessons.router)
app.include_router(admin_tasks.router)
app.include_router(admin_attempts.router)
app.include_router(admin_achievements.router)
app.include_router(achievements.router)
app.include_router(admin_shop.router)
app.include_router(shop.router)

#alembic revision --autogenerate -m "Initial migration"
#alembic upgrade head