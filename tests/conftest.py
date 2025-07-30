# pylint: disable=redefined-outer-name
import asyncio
import uuid

import pytest
import pytest_asyncio
from sqlalchemy import text, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from alembic.config import Config as AlembicConfig
from alembic import command

from app.core.config import settings
from app.db import models
from tests.factory import UserFactory

# 🔧 Генерация уникального URL тестовой базы
TEST_DB_NAME = f"test_{uuid.uuid4().hex[:8]}"
TEST_DATABASE_URL = str(settings.SQLALCHEMY_DATABASE_URI)+TEST_DB_NAME

# 🔄 Асинхронный движок и фабрика сессий
engine = create_async_engine(TEST_DATABASE_URL, future=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

from urllib.parse import urlparse, urlunparse

def get_admin_url(test_url: str) -> str:
    parsed = urlparse(test_url.replace("+asyncpg", "+psycopg2"))
    return urlunparse(parsed._replace(path="/postgres"))


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    # Создаем тестовую базу (через sync pg драйвер)
    sync_url = TEST_DATABASE_URL.replace("+asyncpg", "+psycopg2")
    sync_engine = create_engine(sync_url, future=True)

    with sync_engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT").execute(
            text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}")
        )
        conn.execution_options(isolation_level="AUTOCOMMIT").execute(
            text(f"CREATE DATABASE {TEST_DB_NAME}")
        )
    sync_engine.dispose()

    # Применяем миграции
    alembic_cfg = AlembicConfig("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DATABASE_URL)
    command.upgrade(alembic_cfg, "head")

    yield

    # Удаляем базу
    sync_engine = create_engine(sync_url, future=True)
    with sync_engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT").execute(
            text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}")
        )
    sync_engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def async_session():
    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()

# 🧪 Фабрика пользователей
@pytest_asyncio.fixture
async def user_creator(async_session):
    async def _factory(commit: bool = False, **kwargs):
        return await UserFactory.create(session=async_session, commit=commit, **kwargs)
    return _factory

# ✅ Созданный пользователь
@pytest_asyncio.fixture
async def created_user(user_creator) -> models.User:
    return await user_creator(commit=True)

# 🔀 UUID для тестов
@pytest.fixture
def fake_uuid():
    return uuid.uuid4()

# 🧪 Данные пользователя через Faker
@pytest.fixture
def fake_user_data(faker):
    return {
        "email": faker.unique.email(),
        "username": faker.unique.user_name(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "birthday": faker.date_of_birth(minimum_age=18, maximum_age=70).isoformat(),
        "avatar_url": faker.image_url(),
        "password": faker.password(length=12, special_chars=True, digits=True),
    }
