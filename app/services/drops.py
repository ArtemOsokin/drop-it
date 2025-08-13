import uuid

from app.api.exceptions import drop_exceptions
from app.db.models import Drop
from app.repositories.interfaces import IDropRepository
from app.schemas.drops import DropCreate
from app.services.interfaces import IDropService


class DropService(IDropService):
    def __init__(self, drop_repo: IDropRepository) -> None:
        self.drop_repo = drop_repo

    async def create_drop(self, drop_data: DropCreate, user_id: uuid.UUID) -> Drop:
        if drop_data.genre_id:
            if not await self.drop_repo.get_genre_by_id(drop_data.genre_id):
                raise drop_exceptions.GenreNotFound
        drop = Drop(**drop_data.to_orm_dict(), artist_id=user_id)
        return await self.drop_repo.save_drop(drop)
