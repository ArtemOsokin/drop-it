import pytest

from app.db.models import User
from app.repositories.user import UserRepository


@pytest.fixture
def user_repo(session):
    """Фикстура репозитория пользователей"""
    return UserRepository(db=session)


@pytest.fixture
def fake_user(fake_user_data):
    fake_user_data.update({'hashed_password': fake_user_data.get('password')})
    fake_user_data.pop('password')
    return User(**fake_user_data)
