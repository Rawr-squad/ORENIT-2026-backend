from jose import jwt, JWTError
from fastapi import WebSocket, HTTPException
from sqlalchemy.orm import Session

from app.models.models import User
from app.core.security import SECRET


async def get_user_from_ws(websocket: WebSocket, db: Session):
    token = websocket.query_params.get("token")

    if not token:
        raise HTTPException(401, "Token missing")

    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        user_id = int(payload["sub"])
    except JWTError:
        raise HTTPException(401, "Invalid token")

    user = db.get(User, user_id)

    if not user:
        raise HTTPException(401, "User not found")

    return user