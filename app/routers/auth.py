from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.schemas.auth import RegisterRequest, LoginRequest
from app.core.db import get_db
from app.services.auth import AuthService

router = APIRouter(prefix="/auth")


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return AuthService(db).register(**data.model_dump())


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return AuthService(db).login(**data.model_dump())

@router.get("/me")
def about_user(user = Depends(get_current_user)):
    return {"nickname" : user.nickname,
            "email" : user.email,
            "role" : user.role}
