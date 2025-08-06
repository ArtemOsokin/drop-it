# flake8: noqa: F821
import datetime as dt
import uuid
from typing import List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from app.db.models.base import LAZY_TYPE, IDMixin, TimestampMixin


class Drop(IDMixin, TimestampMixin):
    __tablename__ = "drops"

    artist_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    genre_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("genres.id"), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_url: Mapped[str] = mapped_column(String(1024), nullable=False)
    cover_url: Mapped[str] = mapped_column(String(1024), nullable=True)

    is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_expired: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    artist: Mapped["User"] = relationship(
        "User", back_populates="drops", lazy=LAZY_TYPE, passive_deletes=True
    )
    genre: Mapped["Genre"] = relationship("Genre", back_populates="drops", lazy=LAZY_TYPE)

    expires_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=expression.text("(now() + interval '7 days')"),
    )

    likes: Mapped[List["Like"]] = relationship(
        "Like", back_populates="drop", cascade="all, delete-orphan", lazy=LAZY_TYPE
    )


class Genre(IDMixin, TimestampMixin):
    __tablename__ = "genres"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    drops: Mapped["Drop"] = relationship("Drop", back_populates="genre", lazy=LAZY_TYPE)
