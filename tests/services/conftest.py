# pylint: disable=redefined-outer-name
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from app.repositories.interfaces import IDropRepository, IUserRepository
from app.schemas.auth import PasswordChange, UserLogin
from app.schemas.drops import DropCreate
from app.schemas.users import UserCreate, UserUpdate
from app.services.auth import AuthService
from app.services.drops import DropService
from app.services.users import UserService


@pytest.fixture
def fake_user_create(fake_user_data):
    return UserCreate(**fake_user_data)


@pytest.fixture
def fake_user_update(fake_user_data):
    return UserUpdate(**fake_user_data)


@pytest.fixture
def fake_user_login(fake_login_data):
    return UserLogin(**fake_login_data)


@pytest.fixture
def fake_change_password(faker):
    return PasswordChange(current_password=faker.password(), new_password=faker.password())


@pytest.fixture
def fake_drop_create(fake_drop_data_generator, fake_uuid):
    return DropCreate(**fake_drop_data_generator(genre_id=fake_uuid))


@pytest.fixture
def mock_repo():
    def _factory(interface_cls):
        return AsyncMock(spec=interface_cls)

    return _factory


@pytest.fixture
def mock_user_repo(mock_repo):
    return mock_repo(IUserRepository)


@pytest.fixture
def mock_drop_repo(mock_repo):
    return mock_repo(IDropRepository)


@pytest_asyncio.fixture
async def user_service(mock_user_repo):
    return UserService(user_repo=mock_user_repo)


@pytest_asyncio.fixture
async def auth_service(mock_user_repo):
    return AuthService(user_repo=mock_user_repo)


@pytest_asyncio.fixture
async def drop_service(mock_drop_repo):
    return DropService(drop_repo=mock_drop_repo)
