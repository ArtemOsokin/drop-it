import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    first_name: Optional[str] = Field(None, max_length=30)
    last_name: Optional[str] = Field(None, max_length=30)
    is_artist: bool = False
    birthday: Optional[datetime] = None
    avatar_url: Optional[str] = Field(None, max_length=512)


class UserCreate(UserBase):
    hashed_password: str = Field(..., min_length=5, max_length=100, alias="password")


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=30)
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, max_length=30)
    last_name: Optional[str] = Field(None, max_length=30)
    is_artist: Optional[bool] = None
    birthday: Optional[datetime] = None
    avatar_url: Optional[str] = Field(None, max_length=512)


class UserRead(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    is_active: bool
    is_admin: bool
    is_verified: bool
    last_login: Optional[datetime]
    created_at: datetime
    updated_at: datetime
