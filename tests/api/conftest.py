import pytest
import pytest_asyncio

from httpx import AsyncClient

from app.db.engine import get_async_session
from main import app


@pytest_asyncio.fixture(scope="function")
async def client(async_session):
    if hasattr(async_session, "__anext__"):
        raise ValueError('Not Acync session')
    async def override_get_session():
        yield async_session

    app.dependency_overrides[get_async_session] = override_get_session

    async with AsyncClient() as c:
        yield c

    app.dependency_overrides.clear()
