import uuid
from datetime import datetime, timedelta
from typing import Optional

from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.exceptions.error_messages import HTTPErrorMessage
from app.exceptions.http_exceptions import Unauthorized
from app.schemas.auth import TokenData

# Security settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


class AuthUtils:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Check password"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create refresh token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    def verify_token(token: str, token_type: str = "access") -> TokenData:
        """Token verification"""

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get("sub")
            token_type_payload: str = payload.get("type")

            if user_id is None or token_type_payload != token_type:
                raise Unauthorized(enum_error=HTTPErrorMessage.USER_UNAUTHORIZED)

            token_data = TokenData(user_id=uuid.UUID(user_id))
        except (JWTError, ValueError):
            raise Unauthorized(
                enum_error=HTTPErrorMessage.USER_UNAUTHORIZED
            )  # pylint: disable=W0707

        return token_data
