from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.models import User
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, email, password, role, nickname):
        existing = self.db.query(User).filter(
            (User.email == email) | (User.nickname == nickname)
        ).first()

        if existing:
            raise HTTPException(400, "User already exists")

        user = User(
            email=email,
            password_hash=hash_password(password),
            role=role,
            nickname=nickname
        )

        self.db.add(user)
        self.db.commit()
        return user

    def login(self, email, password):
        user = self.db.query(User).filter_by(email=email).first()

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(400, "Invalid Password")

        return {"access_token": create_access_token(user.id)}
