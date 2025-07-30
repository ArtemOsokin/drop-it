from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions.error_messages import HTTPErrorMessage
from app.core.security import AuthUtils, security
from app.db.engine import get_async_session
from app.repositories.user import UserRepository
from app.api.exceptions.http_exceptions import Unauthorized
from app.db.models import User


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_async_session)
) -> User:
    token_data = AuthUtils.verify_token(token.credentials, token_type="access")
    user = await UserRepository(db).get_user_by_id(token_data.user_id)
    if not user:
        raise Unauthorized(error_code=HTTPErrorMessage.USER_UNAUTHORIZED)
    return user
