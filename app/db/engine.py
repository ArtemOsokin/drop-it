from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session

from app.core.config import settings

engine = create_async_engine(str(settings.SQLALCHEMY_DATABASE_URI), future=True)
async_session = async_sessionmaker(bind=engine, autocommit=False, autoflush=False)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session
