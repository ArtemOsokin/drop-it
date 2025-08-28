import uuid

from app.db.repositories.interfaces import IUserRepository
from app.exceptions import user_exceptions
from app.models.user import User
from app.schemas import users as schemas_users
from app.services.interfaces import IUserService
from app.utils.patch import apply_schema


class UserService(IUserService):
    def __init__(self, user_repo: IUserRepository) -> None:
        self.user_repo = user_repo

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        user = await self.user_repo.get_user_by_id(user_id=user_id)
        if user:
            return user
        raise user_exceptions.UserNotFound

    async def update_user(self, user_data: schemas_users.UserUpdate, user: User) -> User:
        if await self.user_repo.get_user_by_email(email=user_data.email):
            raise user_exceptions.EmailAlreadyExists
        if await self.user_repo.get_user_by_username(username=user_data.username):
            raise user_exceptions.UsernameAlreadyExists
        apply_schema(model=user, schema=user_data)
        return await self.user_repo.save_user(user=user)
