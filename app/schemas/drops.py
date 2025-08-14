import datetime as dt
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, HttpUrl, constr


# ---------- Genre ----------
class GenreBase(BaseModel):
    name: constr(max_length=255)
    slug: constr(max_length=255)


class GenreCreate(GenreBase):
    pass


class GenreUpdate(BaseModel):
    name: Optional[constr(max_length=255)] = None
    slug: Optional[constr(max_length=255)] = None


class GenreRead(GenreBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    created_at: dt.datetime
    updated_at: dt.datetime


# ---------- Drop ----------
class DropBase(BaseModel):
    title: constr(max_length=255)
    description: Optional[str] = None
    file_url: HttpUrl
    cover_url: Optional[HttpUrl] = None
    genre_id: Optional[uuid.UUID] = None


class DropCreate(DropBase):

    def to_orm_dict(self) -> dict:
        """Приведение типов для ORM"""
        d = self.model_dump()
        d["file_url"] = str(d["file_url"])
        d["cover_url"] = str(d["cover_url"])
        return d


# class DropUpdate(BaseModel):
#     title: Optional[constr(max_length=255)] = None
#     description: Optional[str] = None
#     file_url: Optional[HttpUrl] = None
#     cover_url: Optional[HttpUrl] = None
#     genre_id: Optional[uuid.UUID] = None
#     is_archived: Optional[bool] = None
#     is_expired: Optional[bool] = None
#     expires_at: Optional[dt.datetime] = None
#
#
# class DropRead(DropBase):
#     model_config = ConfigDict(from_attributes=True)
#
#     id: uuid.UUID
#     is_archived: bool
#     is_expired: bool
#     expires_at: dt.datetime
#     created_at: dt.datetime
#     updated_at: dt.datetime
#     genre: Optional[GenreRead] = None
#     artist: Optional[UserRead] = None


class GenreOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: constr(max_length=255)
    slug: constr(max_length=255)


class ArtistOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: constr(max_length=30)
    avatar_url: Optional[str] = None
    is_artist: bool


class DropOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: constr(max_length=255)
    description: Optional[str] = None
    file_url: HttpUrl
    cover_url: Optional[HttpUrl] = None
    genre: Optional[GenreOut] = None
    artist: Optional[ArtistOut] = None
    created_at: dt.datetime
    expires_at: dt.datetime
    is_expired: bool
