from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import get_async_session
from app.repositories.users import UserRepository
from app.services.auth import AuthService
from app.services.interfaces import IAuthService, IUserService
from app.services.users import UserService


def get_user_service(db: AsyncSession = Depends(get_async_session)) -> IUserService:
    return UserService(user_repo=UserRepository(db=db))


def get_auth_service(db: AsyncSession = Depends(get_async_session)) -> IAuthService:
    return AuthService(user_repo=UserRepository(db=db))
