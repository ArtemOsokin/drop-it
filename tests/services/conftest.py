from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from app.repositories.user import UserRepository
from app.schemas.auth import UserLogin
from app.schemas.users import UserCreate, UserUpdate
from app.services.auth import AuthService
from app.services.user import UserService


@pytest.fixture
def fake_user_create(fake_user_data):
    return UserCreate(**fake_user_data)


@pytest.fixture
def fake_user_update(fake_user_data):
    return UserUpdate(**fake_user_data)


@pytest.fixture
def fake_user_login(fake_login_data):
    return UserLogin(**fake_login_data)


@pytest_asyncio.fixture
async def user_service():
    return UserService(db=AsyncMock())


@pytest_asyncio.fixture
async def auth_service():
    return AuthService(db=AsyncMock())


@pytest.fixture(name='mock_repo_get_user_by_username')
def mock_repo_get_user_by_username(mocker):
    return mocker.patch.object(UserRepository, 'get_user_by_username', AsyncMock())


@pytest.fixture(name='mock_repo_get_user_by_email')
def mock_repo_get_user_by_email(mocker):
    return mocker.patch.object(UserRepository, 'get_user_by_email', AsyncMock())


@pytest.fixture(name='mock_repo_save_user')
def mock_repo_save_user(mocker):
    return mocker.patch.object(UserRepository, 'save_user', AsyncMock())
