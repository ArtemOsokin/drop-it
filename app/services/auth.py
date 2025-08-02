from app.api.exceptions import auth_exceptions
from app.core.security import AuthUtils
from app.db.models import User
from app.schemas import auth as auth_model
from app.schemas import users as users_model
from app.services.base import BaseServiceUserRepo


class AuthService(BaseServiceUserRepo):

    async def register(self, user_data: users_model.UserCreate) -> auth_model.Token:
        if await self.user_repo.get_user_by_email(email=user_data.email):
            raise auth_exceptions.UserAlreadyExistsEmail
        if await self.user_repo.get_user_by_username(username=user_data.username):
            raise auth_exceptions.UserAlreadyExistsUsername

        user_data.hashed_password = AuthUtils.get_password_hash(user_data.hashed_password)

        user = User(**user_data.model_dump())
        created_user = await self.user_repo.create_user(user)

        token_payload = {"sub": str(created_user.id)}

        return auth_model.Token(
            access_token=AuthUtils.create_access_token(token_payload),
            refresh_token=AuthUtils.create_refresh_token(token_payload),
        )
