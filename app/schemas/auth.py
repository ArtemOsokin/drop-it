import uuid
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.schemas import users as users_schema


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserSighup(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: users_schema.UserRead


class TokenData(BaseModel):
    user_id: Optional[uuid.UUID] = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=5, max_length=100)


class PasswordReset(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6, max_length=100)
