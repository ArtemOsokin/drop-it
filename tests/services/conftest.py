from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from app.repositories.users import UserRepository
from app.schemas.auth import PasswordChange, UserLogin
from app.schemas.users import UserCreate, UserUpdate
from app.services.auth import AuthService
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
def mock_user_repo():
    repo = AsyncMock(spec=UserRepository)
    return repo


@pytest_asyncio.fixture
async def user_service(mock_user_repo):
    return UserService(user_repo=mock_user_repo)


@pytest_asyncio.fixture
async def auth_service(mock_user_repo):
    return AuthService(user_repo=mock_user_repo)
