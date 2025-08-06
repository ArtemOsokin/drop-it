from app.db.models import Drop
from app.repositories.base import BaseRepository
from app.repositories.interfaces import IDropRepository


class DropRepository(BaseRepository, IDropRepository):

    async def save_drop(self, drop: Drop) -> Drop:
        self.db.add(drop)
        await self.db.commit()
        await self.db.refresh(drop)
        return drop
