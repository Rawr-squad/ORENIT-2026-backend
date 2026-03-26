from pydantic import BaseModel
from typing import Literal


class RegisterRequest(BaseModel):
    email: str
    password: str
    role: Literal["student", "parent"]


class LoginRequest(BaseModel):
    email: str
    password: str