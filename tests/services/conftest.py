import pytest
import pytest_asyncio

from app.schemas.users import UserCreate
from app.services.auth import AuthService
from app.services.user import UserService


@pytest.fixture
def fake_user_create(fake_user_data):
    return UserCreate(**fake_user_data)


@pytest_asyncio.fixture
async def user_service(session):
    """Создает сервис пользователей"""
    return UserService(db=session)


@pytest_asyncio.fixture
async def auth_service(session):
    """Создает сервис пользователей"""
    return AuthService(db=session)
