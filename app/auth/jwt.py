from datetime import timedelta, datetime
from jose import jwt

from app.settings import settings

ALGORITHM = "HS256"

def create_access_token(data: dict, expires_minutes : int = 30):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp" : expire})

    return jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=ALGORITHM
    )