# pylint: disable=unused-argument,too-many-positional-arguments
from unittest.mock import AsyncMock

import pytest
from fastapi import status
from httpx import AsyncClient, ASGITransport
from sqlalchemy.exc import OperationalError
from fastapi.testclient import TestClient

from app.db.engine import engine
from app.exceptions.error_messages import HTTPErrorMessage
from main import app

pytestmark = pytest.mark.asyncio

@pytest.mark.usefixtures('apply_migrations')
async def test_health(session, client):
    response = await client.get("v1/health-check/healthz")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status': 'ok'}


@pytest.mark.asyncio
async def test_health_error(client: AsyncClient, test_app):
    from app.db.engine import get_async_session
    from unittest.mock import AsyncMock

    mock_session = AsyncMock()
    mock_session.execute.side_effect = OperationalError("mock", None, None)

    async def override_get_async_session():
        yield mock_session

    test_app.dependency_overrides[get_async_session] = override_get_async_session

    response = await client.get("/v1/health-check/healthz")

    assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
    print(response.json())
    assert response.json() == HTTPErrorMessage.DB_UNAVAILABLE

    test_app.dependency_overrides.clear()