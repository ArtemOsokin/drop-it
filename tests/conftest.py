import datetime
import os
import uuid
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from alembic import command
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.config import settings as base_settings
from app.db.models.base import Base
from app.db.models.user import User
from app.repositories.user import UserRepository

TEST_DB_NAME_PREFIX = f"_test_{uuid.uuid4().hex[:8]}"
TEST_DB_NAME = f"{base_settings.POSTGRES_DB+TEST_DB_NAME_PREFIX}"
TEST_DATABASE_URL = base_settings.POSTGRES_URI + TEST_DB_NAME_PREFIX


@pytest_asyncio.fixture(scope="function")
async def engine_test():
    from sqlalchemy.ext.asyncio import create_async_engine

    engine_test = create_async_engine(TEST_DATABASE_URL, future=True)
    yield engine_test
    await engine_test.dispose()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Создание и удаление тестовой БД"""
    import psycopg2

    # Подключаемся к postgres и создаем отдельную тестовую БД
    admin_url = str(base_settings.SQLALCHEMY_DATABASE_URI).replace("+asyncpg", "")
    conn = psycopg2.connect(admin_url)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}")
    cur.execute(f"CREATE DATABASE {TEST_DB_NAME}")
    conn.close()

    yield

    # Удаление БД после тестов
    conn = psycopg2.connect(admin_url)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(
        f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{TEST_DB_NAME}'
              AND pid <> pg_backend_pid();
        """
    )
    cur.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}")
    conn.close()


@pytest.fixture(scope="session")
def apply_migrations(setup_test_db):
    """Применяет миграции alembic к временной тестовой БД"""

    from pathlib import Path

    from alembic.config import Config

    os.environ["POSTGRES_URI"] = TEST_DATABASE_URL.replace("+asyncpg", "+psycopg2")
    alembic_cfg = Config(str(Path(__file__).parent.parent / "alembic.ini"))

    command.upgrade(alembic_cfg, "head")

    yield
    command.downgrade(alembic_cfg, "base")


@pytest_asyncio.fixture(scope="function")
async def session(engine_test):
    """Асинхронная сессия для работы с БД"""
    async_session_test = async_sessionmaker(bind=engine_test, expire_on_commit=False)
    async with async_session_test() as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def clean_tables(session):
    # Получаем все таблицы из metadata
    tables = reversed(Base.metadata.sorted_tables)
    # Отключаем внешние ключи и очищаем таблицы по очереди
    async with session.begin():
        for table in tables:
            await session.execute(text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE"))
    await session.commit()
    yield


@pytest.fixture
def fake_uuid():
    return uuid.uuid4()


@pytest.fixture
def fake_update_user_data(faker):
    return {
        "email": faker.unique.email(),
        "username": faker.unique.user_name(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "birthday": faker.date_of_birth(minimum_age=18, maximum_age=70).isoformat(),
        "avatar_url": faker.image_url(),
        "is_artist": False,
    }


@pytest.fixture
def fake_user_data(faker, fake_update_user_data):
    data = fake_update_user_data.copy()
    data.update(
        {
            "password": faker.password(length=12, special_chars=True, digits=True),
            "is_active": True,
            "is_verified": True,
            "is_admin": False,
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
        }
    )
    return data


@pytest.fixture
def fake_user(fake_user_data):
    """Создает экземпляр модели User для тестов"""
    data = fake_user_data.copy()
    data["birthday"] = datetime.datetime.fromisoformat(data["birthday"])
    data['hashed_password'] = data.pop('password')
    data['id'] = uuid.uuid4()
    return User(**data)


@pytest.fixture
def fake_login_data(fake_user_data):
    return {
        'username': fake_user_data['username'],
        'password': fake_user_data['password'],
    }


@pytest.fixture(name='mock_repo_get_user_by_id')
def mock_repo_get_user_by_id(mocker):
    return mocker.patch.object(UserRepository, 'get_user_by_id', AsyncMock())
