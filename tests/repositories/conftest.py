import datetime

import pytest
import pytest_asyncio

from app.db import models
from app.repositories.user import UserRepository


@pytest_asyncio.fixture
async def user_repo(session):
    """Создает репозиторий пользователей"""
    return UserRepository(db=session)


@pytest.fixture
def fake_user(fake_user_data):
    """Создает экземпляр модели User для тестов"""
    data = fake_user_data.copy()
    data["birthday"] = datetime.datetime.fromisoformat(data["birthday"])
    data['hashed_password'] = data.pop('password')
    return models.User(**data)
