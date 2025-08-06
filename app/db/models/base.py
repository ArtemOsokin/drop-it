import datetime as dt
import uuid

from sqlalchemy import func
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

LAZY_TYPE = 'raise'


class Base(DeclarativeBase):
    pass


class IDMixin(Base):
    __abstract__ = True

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)


# pylint: disable=E1102
class TimestampMixin:
    __abstract__ = True

    created_at: Mapped[dt.datetime] = mapped_column(server_default=func.now(), nullable=False)
    updated_at: Mapped[dt.datetime] = mapped_column(
        server_default=func.now(), nullable=False, onupdate=func.now()
    )
