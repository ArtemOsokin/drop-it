from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from app.repositories.user import UserRepository
from app.schemas.auth import UserLogin
from app.schemas.users import UserCreate
from app.services.auth import AuthService
from app.services.user import UserService


@pytest.fixture
def fake_user_create(fake_user_data):
    return UserCreate(**fake_user_data)


@pytest.fixture
def fake_user_login(fake_login_data):
    return UserLogin(**fake_login_data)


@pytest_asyncio.fixture
async def user_service(session):
    return UserService(db=session)


@pytest_asyncio.fixture
async def auth_service(session):
    return AuthService(db=session)


@pytest.fixture(name='mock_repo_get_user_by_username')
def mock_repo_get_user_by_username(mocker):
    return mocker.patch.object(UserRepository, 'get_user_by_username', AsyncMock())


@pytest.fixture(name='mock_repo_get_user_by_email')
def mock_repo_get_user_by_email(mocker):
    return mocker.patch.object(UserRepository, 'get_user_by_email', AsyncMock())
