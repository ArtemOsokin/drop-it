import logging
import uuid

from app.api.exceptions import user_exceptions
from app.db.models.user import User
from app.schemas import users as schemas_users
from app.services.base import BaseServiceUserRepo

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)


class UserService(BaseServiceUserRepo):

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
