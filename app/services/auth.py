from app.api.exceptions import auth_exceptions
from app.core.security import AuthUtils
from app.db.models import User
from app.schemas import auth as auth_model
from app.schemas import users as users_model
from app.services.base import BaseServiceUserRepo


class AuthService(BaseServiceUserRepo):

    @staticmethod
    def _create_tokens(user_id: str) -> dict:
        token_payload = {"sub": user_id}

        return {
            'access_token': AuthUtils.create_access_token(token_payload),
            'refresh_token': AuthUtils.create_refresh_token(token_payload),
        }

    async def register(self, user_data: users_model.UserCreate) -> dict:
        if await self.user_repo.get_user_by_email(email=user_data.email):
            raise auth_exceptions.UserAlreadyExistsEmail
        if await self.user_repo.get_user_by_username(username=user_data.username):
            raise auth_exceptions.UserAlreadyExistsUsername

        user_data.hashed_password = AuthUtils.get_password_hash(user_data.hashed_password)

        user = User(**user_data.model_dump())
        created_user = await self.user_repo.save_user(user)
        return self._create_tokens(str(created_user))

    async def login(self, login_data: auth_model.UserLogin) -> dict:
        user = await self.user_repo.get_user_by_username(username=login_data.username)
        if not user:
            raise auth_exceptions.IncorrectUsername

        if not AuthUtils.verify_password(login_data.password, user.hashed_password):
            raise auth_exceptions.IncorrectPassword

        return self._create_tokens(user_id=str(user.id))

    async def change_password(self, pass_data: auth_model.PasswordChange, user: User) -> None:
        if not AuthUtils.verify_password(pass_data.current_password, user.hashed_password):
            raise auth_exceptions.IncorrectPassword

        user.hashed_password = AuthUtils.get_password_hash(pass_data.new_password)

        await self.user_repo.save_user(user)
