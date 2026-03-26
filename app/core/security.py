from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

SECRET = "SECRET"
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)


def create_access_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=60),
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)