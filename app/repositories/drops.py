from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import Drop, Genre
from app.repositories.base import BaseRepository
from app.repositories.interfaces import IDropRepository


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

        return result.scalar_one()
