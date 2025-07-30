import pytest
import pytest_asyncio

from app.db.models import User
from app.repositories.user import UserRepository


@pytest_asyncio.fixture
async def user_repo(async_session):
    if hasattr(async_session, "__anext__"):
        raise ValueError('Not Acync session')
    """Фикстура репозитория пользователей"""
    return UserRepository(db=async_session)


@pytest.fixture
def fake_user(fake_user_data):
    data = fake_user_data.copy()
    data['hashed_password'] = data.pop('password')
    return User(**data)
