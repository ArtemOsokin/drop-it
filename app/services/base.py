from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user import UserRepository


class BaseService:
    pass


class BaseServiceUserRepo(BaseService):
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
