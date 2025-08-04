import pytest_asyncio

from app.db import models
from app.repositories.user import UserRepository
from tests.factory import UserFactory


@pytest_asyncio.fixture
async def user_creator(session):
    async def _factory(commit: bool = False, **kwargs):
        user = await UserFactory.create(session=session, commit=commit, **kwargs)
        return user

    return _factory


@pytest_asyncio.fixture
async def created_user(user_creator) -> models.User:
    return await user_creator(commit=True)


@pytest_asyncio.fixture
async def user_repo(session):
    """Создает репозиторий пользователей"""
    return UserRepository(db=session)
