from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.auth import RegisterRequest, LoginRequest, TokenResponse
from app.database.dao.user import UserDAO
from app.database.dependencies import get_db

from app.auth.security import hash_password, verify_password
from app.auth.jwt import create_access_token


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register")
async def register(
    data: RegisterRequest,
    db: AsyncSession = Depends(get_db)
):

    existing = await UserDAO.find_one(db, username=data.username)

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    user = await UserDAO.add(db, username=data.username, password_hash=hash_password(data.password))

    return user


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):

    user = await UserDAO.find_one(db, username=data.username)

    if not user:
        raise HTTPException(401)

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(401)

    token = create_access_token(
        {"sub": str(user.id)}
    )

    return {"access_token": token}