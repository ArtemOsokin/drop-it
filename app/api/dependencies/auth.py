from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.error_messages import HTTPErrorMessage
from app.api.exceptions.http_exceptions import Unauthorized
from app.core.security import AuthUtils, security
from app.db.engine import get_async_session
from app.db.models.user import User
from app.repositories.interfaces import IUserRepository
from app.repositories.users import UserRepository


def get_user_repository(db: AsyncSession = Depends(get_async_session)) -> IUserRepository:
    return UserRepository(db)


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    user_repo: IUserRepository = Depends(get_user_repository),
) -> User:
    token_data = AuthUtils.verify_token(token.credentials, token_type="access")
    user = await user_repo.get_user_by_id(token_data.user_id)
    if not user:
        raise Unauthorized(enum_error=HTTPErrorMessage.USER_UNAUTHORIZED)
    return user
