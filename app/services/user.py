import logging
import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.exceptions import user_exceptions
from app.db.models import User
from app.repositories.user import UserRepository
from app.services.base import BaseService

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)


class UserService(BaseService):
    def __init__(self, db: Optional[AsyncSession] = None):
        self._db = db
        self._user_repo = None

    @property
    def user_repo(self) -> UserRepository:
        if not self._user_repo:
            if not self._db:
                raise RuntimeError("DB session not available")
            self._user_repo = UserRepository(self._db)
        return self._user_repo

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        user = await self.user_repo.get_user_by_id(user_id=user_id)
        print('=-=-=',user)
        if user:
            return user
        raise user_exceptions.UserNotFound
