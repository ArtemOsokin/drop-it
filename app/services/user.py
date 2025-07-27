import logging
import uuid

from sqlalchemy.orm import Session as SessionType

from app.api.exceptions.user_exceptions import UserNotFound
from app.db.models import User
from app.repositories.user import UserRepository
from app.services.base import BaseServiceDB

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)


class UserService(BaseServiceDB):

    async def get_user_by_id(self, user_id: uuid.UUID, db: SessionType) -> User:
        user_repo = UserRepository(db=db)
        user = user_repo.get_user_by_id(user_id=user_id)
        if user:
            return user
        raise UserNotFound
