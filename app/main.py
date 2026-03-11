from fastapi import FastAPI

from app.routes import users, auth

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)

# docker compose up --build
# alembic revision --autogenerate -m ".."
# alembic upgrade head