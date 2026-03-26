from fastapi import Depends, HTTPException, status, Header
from jose import jwt
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.models import User
from app.core.security import SECRET


def get_current_user(
        authorization: str = Header(None, alias="Authorization"),
        db: Session = Depends(get_db)
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    # Проверяем формат "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization format")

    token = parts[1]

    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user = db.get(User, int(payload["sub"]))
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def require_role(required_roles: list[str]):
    def wrapper(user: User = Depends(get_current_user)):
        if user.role not in required_roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return user
    return wrapper