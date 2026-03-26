from sqlalchemy.orm import Session
from app.models.models import User
from app.core.security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register(self, email, password, role):
        user = User(
            email=email,
            password_hash=hash_password(password),
            role=role,
        )
        self.db.add(user)
        self.db.commit()
        return user

    def login(self, email, password):
        user = self.db.query(User).filter_by(email=email).first()

        if not user or not verify_password(password, user.password_hash):
            raise Exception("Invalid")

        return {"access_token": create_access_token(user.id)}