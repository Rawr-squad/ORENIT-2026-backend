from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserRead
from app.database.dao.user import UserDAO, User
from app.database.dependencies import get_db
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserRead)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):

    return await UserDAO.add(
        session=db,
        **user.model_dump()
    )


@router.get("/", response_model=list[UserRead])
async def get_users(
    db: AsyncSession = Depends(get_db)
):

    return await UserDAO.find_all(
        session=db
    )

@router.get('/me')
async def get_user_info(user = Depends(get_current_user)):
    return user