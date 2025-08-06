# Фикстуры для API тестов
from typing import AsyncGenerator
from unittest.mock import AsyncMock

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from app.api.dependencies.auth import get_current_user
from app.api.exceptions.error_messages import HTTPErrorMessage
from app.api.exceptions.http_exceptions import BadRequest, Unauthorized
from app.core.security import AuthUtils
from app.repositories.interfaces import IUserRepository
from app.services.auth import AuthService
from app.services.users import UserService
from main import app


@pytest_asyncio.fixture
async def fake_token():
    class FakeToken:
        """Заменяет HTTPAuthorizationCredentials"""

        def __init__(self, token: str):
            self.credentials = token

    return FakeToken


@pytest_asyncio.fixture
async def override_get_async_session(session):
    """Override для dependency injection базы данных"""

    async def _override_get_async_session():
        yield session

    return _override_get_async_session


@pytest_asyncio.fixture
async def test_app(override_get_async_session):
    """Создает тестовое приложение с переопределенными зависимостями"""
    from app.db.engine import get_async_session

    app.dependency_overrides[get_async_session] = override_get_async_session
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(test_app) -> AsyncGenerator[AsyncClient, None]:
    """Создает HTTP клиент для API тестов"""
    async with AsyncClient(transport=ASGITransport(app=test_app), base_url="http://test") as c:
        yield c


@pytest.fixture(name='mock_service_get_user_by_id')
def mock_service_get_user_by_id(mocker):
    return mocker.patch.object(UserService, 'get_user_by_id', AsyncMock())


@pytest.fixture(name='mock_service_update_user')
def mock_service_update_user(mocker):
    return mocker.patch.object(UserService, 'update_user', AsyncMock())


@pytest.fixture(name='mock_service_register')
def mock_service_register(mocker):
    return mocker.patch.object(AuthService, 'register', AsyncMock())


@pytest.fixture(name='mock_service_login')
def mock_service_login(mocker):
    return mocker.patch.object(AuthService, 'login', AsyncMock())


@pytest.fixture(name='mock_service_change_password')
def mock_service_change_password(mocker):
    return mocker.patch.object(AuthService, 'change_password', AsyncMock())


@pytest_asyncio.fixture
async def override_get_current_user(test_app, fake_user):

    test_app.dependency_overrides[get_current_user] = lambda: fake_user
    yield
    test_app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def override_get_current_user_unauthorized(test_app):
    def raise_unauthorized():
        raise Unauthorized(enum_error=BadRequest(enum_error=HTTPErrorMessage.USER_UNAUTHORIZED))

    test_app.dependency_overrides[get_current_user] = raise_unauthorized
    yield
    test_app.dependency_overrides.clear()


@pytest.fixture
def fake_token_data(fake_uuid) -> str:
    payload = {"sub": str(fake_uuid)}
    return {
        "access_token": AuthUtils.create_access_token(payload),
        "refresh_token": AuthUtils.create_refresh_token(payload),
    }


@pytest.fixture
def fake_user_data_request(fake_user_data):
    fake_user_data['created_at'] = fake_user_data['created_at'].isoformat()
    fake_user_data['updated_at'] = fake_user_data['updated_at'].isoformat()
    return fake_user_data


@pytest.fixture(name='mock_user_repo')
def mock_user_repo():
    repo = AsyncMock(spec=IUserRepository)
    repo.get_user_by_id = AsyncMock(return_value=None)
    return repo
