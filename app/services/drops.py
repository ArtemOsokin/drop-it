import uuid

from app.db.repositories.interfaces import IDropRepository
from app.exceptions import drop_exceptions
from app.models import Drop, Genre
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

    async def get_drop_by_id(self, drop_id: uuid.UUID) -> Drop:
        drop = await self.drop_repo.get_drop_by_id(drop_id=drop_id)
        if not drop:
            raise drop_exceptions.DropNotFound
        return drop

    async def list_genres(self) -> list[Genre]:
        return await self.drop_repo.list_genres()

    async def list_drops(
        self, page: int, page_size: int, genre_id: str = None, artist_id: str = None
    ) -> (list[Drop], int):
        drops = await self.drop_repo.list_drops(
            page=page,
            page_size=page_size,
            genre_id=genre_id,
            artist_id=artist_id,
        )
        total = await self.drop_repo.count_drops(genre_id=genre_id, artist_id=artist_id)
        return drops, total
