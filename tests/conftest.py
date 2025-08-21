# pylint: disable=redefined-outer-name,import-outside-toplevel,unused-argument
import datetime as dt
import os
import uuid

import pytest
import pytest_asyncio
from alembic import command
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.core.config import settings as base_settings
from app.models import Drop, Genre
from app.models.base import Base
from app.models.user import User
from tests.factory import GenreFactory, UserFactory

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


# ==== Faker Fixtures ====


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
            "created_at": dt.datetime.now(),
            "updated_at": dt.datetime.now(),
        }
    )
    return data


@pytest_asyncio.fixture
async def fake_user() -> User:
    return await UserFactory.create()


@pytest_asyncio.fixture
async def fake_user_with_meta(fake_user, fake_uuid) -> User:
    fake_user.id = fake_uuid
    fake_user.updated_at = dt.datetime.now(dt.timezone.utc)
    fake_user.created_at = dt.datetime.now(dt.timezone.utc)
    return fake_user


@pytest.fixture
def fake_genre_data(faker):
    """Генерирует словарь с данными для Genre"""
    return {
        "name": faker.word(),
        "slug": faker.slug(),
        "created_at": dt.datetime.now(dt.timezone.utc),
        "updated_at": dt.datetime.now(dt.timezone.utc),
    }


@pytest_asyncio.fixture
async def fake_genre(fake_uuid) -> Genre:
    return await GenreFactory.create(id=fake_uuid)


@pytest.fixture
def fake_drop_data_generator(faker):
    """Универсальный генератор данных для Drop"""

    def _generate(genre_id=None, artist_id=None):
        return {
            "artist_id": artist_id if artist_id else None,
            "genre_id": genre_id if genre_id else None,
            "title": faker.sentence(nb_words=4),
            "description": faker.text(max_nb_chars=200),
            "file_url": faker.url(),
            "cover_url": faker.url(),
            "is_archived": False,
            "is_expired": False,
            "expires_at": dt.datetime.now() + dt.timedelta(days=7),
            "created_at": dt.datetime.now(),
            "updated_at": dt.datetime.now(),
        }

    return _generate


@pytest.fixture
def fake_drop(fake_drop_data_generator, fake_user, fake_genre) -> Drop:
    """Создает экземпляр Genre"""
    data = fake_drop_data_generator(artist_id=fake_user.id, genre_id=fake_genre.id)
    data["id"] = uuid.uuid4()
    return Drop(**data)


@pytest.fixture
def fake_login_data(fake_user_data):
    return {
        'username': fake_user_data['username'],
        'password': fake_user_data['password'],
    }
