from pydantic import BaseModel, EmailStr
from typing import Literal


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    nickname : str
    role: Literal["student", "parent"]


class LoginRequest(BaseModel):
    email: str
    password: str