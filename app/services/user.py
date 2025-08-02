import logging
import uuid

from app.api.exceptions import user_exceptions
from app.db.models import User
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
