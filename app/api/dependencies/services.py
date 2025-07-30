from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.engine import get_async_session
from app.services.auth import AuthService
from app.services.user import UserService

def get_user_service(db: AsyncSession = Depends(get_async_session)) -> UserService:
    return UserService(db=db)

def get_auth_service(db: AsyncSession = Depends(get_async_session)) -> AuthService:
    return AuthService(db=db)