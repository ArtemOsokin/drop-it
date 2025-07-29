from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials

from app.api.exceptions.error_messages import HTTPErrorMessage
from app.core.security import AuthUtils, security
from app.db.engine import get_db
from app.repositories.user import UserRepository
from app.api.exceptions.http_exceptions import Unauthorized
from sqlalchemy.orm import Session
from app.db.models import User


def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    token_data = AuthUtils.verify_token(token.credentials, token_type="access")
    user = UserRepository(db).get_user_by_id(token_data.user_id)
    if not user:
        raise Unauthorized(error_code=HTTPErrorMessage.USER_UNAUTHORIZED)
    return user
