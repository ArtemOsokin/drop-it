# Фикстуры для API тестов
from typing import AsyncGenerator

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from main import app


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
