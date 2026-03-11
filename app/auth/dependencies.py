from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from sqlalchemy.ext.asyncio import AsyncSession

from app.settings import settings
from app.database.dao.user import UserDAO
from app.database.dependencies import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token : str = Depends(oauth2_scheme), db : AsyncSession = Depends(get_db)):

    try:
        payload = jwt.decode(token=token, key=settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await UserDAO.find_by_id(session=db, id=int(user_id))

    if not user:
        raise HTTPException(401)

    return user
