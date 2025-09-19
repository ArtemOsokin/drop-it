# flake8: noqa: F821
import datetime as dt
import uuid
from typing import List

from sqlalchemy import Boolean, DateTime, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.security import AuthUtils
from app.models.base import LAZY_TYPE, IDMixin, TimestampMixin


class User(IDMixin, TimestampMixin):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(30), unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(30), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(30), nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)

    is_artist: Mapped[bool] = mapped_column(Boolean, default=False)
    birthday: Mapped[dt.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    avatar_url: Mapped[str | None] = mapped_column(String(512), nullable=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=True)

    last_login: Mapped[dt.datetime | None] = mapped_column(DateTime, nullable=True)

    drops: Mapped[List["Drop"]] = relationship(
        "Drop",
        back_populates="artist",
        cascade="all, delete-orphan",
        lazy=LAZY_TYPE,
        passive_deletes=True,
    )
    likes: Mapped[List["Like"]] = relationship(
        "Like",
        back_populates="user",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy=LAZY_TYPE,
    )

    def __repr__(self) -> str:
        return f"<User {self.username}>"


class Like(IDMixin):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint('user_id', 'drop_id', name='uix_user_drop'),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    drop_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("drops.id", ondelete="CASCADE"), nullable=False, index=True
    )

    created_at: Mapped[dt.datetime] = mapped_column(
        DateTime(timezone=True), default=func.now, nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="likes", lazy=LAZY_TYPE)
    drop: Mapped["Drop"] = relationship("Drop", back_populates="likes", lazy=LAZY_TYPE)
