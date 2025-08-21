from typing import Generic, List, TypeVar

from pydantic import BaseModel, Field

from app.core.config import settings

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int = Field(1, ge=1)
    page_size: int = Field(
        settings.PAGINATION_DEFAULT_PAGE_SIZE,
        ge=settings.PAGINATION_MIN_PAGE_SIZE,
        le=settings.PAGINATION_MAX_PAGE_SIZE,
    )
