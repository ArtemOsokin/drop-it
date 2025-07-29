# pylint: disable=redefined-outer-name
import subprocess
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists, drop_database

from app.core.config import settings
from app.db import models
from app.db.base import Base
from app.db.models import User
from tests.factory import UserFactory


@pytest.fixture(scope="session")
def apply_migrations():
    subprocess.run(["alembic", "upgrade", "head"], check=True)
    yield
    subprocess.run(["alembic", "downgrade", "base"], check=True)


@pytest.fixture(scope="session")
def test_db_url():
    url = str(settings.SQLALCHEMY_DATABASE_URI) + "_test"
    if not database_exists(url):
        create_database(url)
    return url


@pytest.fixture(scope="session")
def engine(test_db_url):
    engine = create_engine(test_db_url)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    drop_database(test_db_url)


@pytest.fixture(scope="function")
def session(engine):
    testing_session_local = sessionmaker(bind=engine)
    session = testing_session_local()
    yield session
    session.rollback()
    session.close()


@pytest.fixture(autouse=True)
def clean_tables(session):
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()


@pytest.fixture
def user_creator(session):
    def _factory(**kwargs):
        UserFactory._meta.sqlalchemy_session = session  # pylint: disable=W0212
        return UserFactory(**kwargs)

    return _factory


@pytest.fixture
def created_user(user_creator) -> models.User:
    return user_creator()


@pytest.fixture
def fake_uuid():
    return uuid.uuid4()

@pytest.fixture
def fake_user_data(faker):
    """Генерация данных пользователя через Faker"""
    return {
        "email": faker.unique.email(),
        "username": faker.unique.user_name(),
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "birthday": faker.date_of_birth(minimum_age=18, maximum_age=70).isoformat(),
        "avatar_url": faker.image_url(),
        "password": faker.password(length=12, special_chars=True, digits=True),
    }