from sqlalchemy import func, select
from sqlalchemy.orm import joinedload, selectinload

from app.core.config import settings
from app.db.query_builders.drops import DropQueryBuilder
from app.db.repositories.base import BaseRepository
from app.db.repositories.interfaces import IDropRepository
from app.models import Drop, Genre


class DropRepository(BaseRepository, IDropRepository):

    async def save_drop(self, drop: Drop) -> Drop:
        self.db.add(drop)
        await self.db.commit()
        await self.db.refresh(drop)
        return await self.get_drop_by_id(drop_id=drop.id)

    async def get_genre_by_id(self, genre_id: str) -> Genre:
        result = await self.db.execute(select(Genre).where(Genre.id == genre_id))
        return result.scalar_one_or_none()

    async def get_drop_by_id(self, drop_id: str) -> Drop:
        stmt = (
            select(Drop)
            .options(selectinload(Drop.genre), selectinload(Drop.artist))
            .where(Drop.id == drop_id)
        )
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def list_genres(self) -> list[Genre]:
        result = await self.db.execute(select(Genre))
        return result.scalars().all()

    async def list_drops(
        self,
        page: int = 1,
        page_size: int = settings.PAGINATION_DEFAULT_PAGE_SIZE,
        genre_id: str = None,
        artist_id: str = None,
    ) -> list[Drop]:

        query = (
            DropQueryBuilder()
            .filter_by_genre(genre_id)
            .filter_by_artist(artist_id)
            .order_by_created()
            .limit_offset(page, page_size)
            .build()
            .options(joinedload(Drop.genre), joinedload(Drop.artist))
        )

        result = await self.db.execute(query)
        return result.scalars().all()

    async def count_drops(self, genre_id: str = None, artist_id: str = None) -> int:
        query = (
            DropQueryBuilder(select(func.count()).select_from(Drop))
            .filter_by_genre(genre_id)
            .filter_by_artist(artist_id)
            .build()
        )

        return await self.db.scalar(query)
