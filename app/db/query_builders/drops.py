from sqlalchemy import Select, select

from app.core.config import settings
from app.models import Drop


class DropQueryBuilder:
    def __init__(self, base_query: Select | None = None):
        if base_query is None:
            base_query = select(Drop)
        self.query = base_query.where(Drop.is_archived.is_(False))

    def filter_by_genre(self, genre_id: str | None):
        if genre_id:
            self.query = self.query.where(Drop.genre_id == genre_id)
        return self

    def filter_by_artist(self, artist_id: str | None):
        if artist_id:
            self.query = self.query.where(Drop.artist_id == artist_id)
        return self

    def order_by_created(self, desc: bool = True):
        if desc:
            self.query = self.query.order_by(Drop.created_at.desc())
        else:
            self.query = self.query.order_by(Drop.created_at.asc())
        return self

    def limit_offset(self, page: int = 1, page_size: int = settings.PAGINATION_DEFAULT_PAGE_SIZE):
        self.query = self.query.limit(page_size).offset((page - 1) * page_size)
        return self

    def build(self) -> Select:
        return self.query
