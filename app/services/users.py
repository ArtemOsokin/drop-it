import uuid

from app.db.repositories.interfaces import IUserRepository
from app.exceptions import user_exceptions
from app.models.user import User
from app.schemas import users as schemas_users


class UserService:
    def __init__(self, user_repo: IUserRepository) -> None:
        self.user_repo = user_repo

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        user = await self.user_repo.get_user_by_id(user_id=user_id)
        if user:
            return user
        raise user_exceptions.UserNotFound

    async def update_user(self, update_data: schemas_users.UserUpdate, user: User) -> User:
        if await self.user_repo.get_user_by_email(email=update_data.email):
            raise user_exceptions.EmailAlreadyExists
        if await self.user_repo.get_user_by_username(username=update_data.username):
            raise user_exceptions.UsernameAlreadyExists
        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)
        return await self.user_repo.save_user(user=user)
