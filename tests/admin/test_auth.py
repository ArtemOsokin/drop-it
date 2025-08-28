from unittest.mock import AsyncMock, patch

import pytest
from starlette.datastructures import FormData
from starlette.requests import Request

from app.admin.auth import AdminAuth, auth_exceptions

pytestmark = pytest.mark.asyncio


async def test_login_success():
    request = AsyncMock(spec=Request)
    request.form = AsyncMock(return_value=FormData({"username": "test", "password": "secret"}))
    request.session = {}

    mock_user = AsyncMock(id=1)
    with patch("app.admin.auth.AuthService") as mock_auth_service:
        instance = mock_auth_service.return_value
        instance.login_admin = AsyncMock(return_value=mock_user)

        auth = AdminAuth(secret_key="dummy")
        result = await auth.login(request)

    assert result is True
    assert request.session["admin_id"] == "1"


async def test_login_incorrect_credentials():
    request = AsyncMock(spec=Request)
    request.form = AsyncMock(return_value=FormData({"username": "bad", "password": "wrong"}))
    request.session = {}

    with patch("app.admin.auth.AuthService") as mock_auth_service:
        instance = mock_auth_service.return_value
        instance.login_admin = AsyncMock(side_effect=auth_exceptions.IncorrectUsername)

        auth = AdminAuth(secret_key="dummy")
        result = await auth.login(request)

    assert result is False
    assert not request.session


async def test_logout_clears_session():
    request = AsyncMock(spec=Request)
    request.session = {"admin_id": "1"}

    auth = AdminAuth(secret_key="dummy")
    result = await auth.logout(request)

    assert result is True
    assert not request.session


async def test_authenticate_redirect():
    request = AsyncMock(spec=Request)
    request.session = {}
    request.url_for.return_value = "/login"

    auth = AdminAuth(secret_key="dummy")
    response = await auth.authenticate(request)

    assert response.status_code == 302
    assert response.headers["location"] == "/login"
