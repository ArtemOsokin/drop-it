# pylint: disable=redefined-outer-name
import pytest_asyncio

from app.db.models.user import User
from app.repositories.drops import DropRepository
from app.repositories.interfaces import IDropRepository, IUserRepository
from app.repositories.users import UserRepository
from tests.factory import GenreFactory, UserFactory


@pytest_asyncio.fixture
async def user_creator(session):
    async def _factory(commit: bool = False, **kwargs):
        user = await UserFactory.create(session=session, commit=commit, **kwargs)
        return user

    return _factory


@pytest_asyncio.fixture
async def created_user(user_creator) -> User:
    return await user_creator(commit=True)


@pytest_asyncio.fixture
async def genre_creator(session):
    async def _factory(commit: bool = False, **kwargs):
        genre = await GenreFactory.create(session=session, commit=commit, **kwargs)
        return genre

    return _factory


@pytest_asyncio.fixture
async def created_genre(genre_creator) -> User:
    return await genre_creator(commit=True)


@pytest_asyncio.fixture
async def user_repo(session) -> IUserRepository:
    """Создает репозиторий пользователей"""
    return UserRepository(db=session)


@pytest_asyncio.fixture
async def drop_repo(session) -> IDropRepository:
    """Создает репозиторий пользователей"""
    return DropRepository(db=session)
