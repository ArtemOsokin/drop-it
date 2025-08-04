from unittest.mock import AsyncMock

import pytest

from app.api.dependencies.auth import get_current_user  # путь адаптируй под себя
from app.api.exceptions.http_exceptions import Unauthorized
from app.core.security import AuthUtils

pytestmark = pytest.mark.asyncio


async def test_get_current_user_valid(fake_token, mock_repo_get_user_by_id, fake_user):
    mock_repo_get_user_by_id.return_value = fake_user
    access_token = AuthUtils.create_access_token({"sub": str(fake_user.id)})
    fake_token = fake_token(access_token)
    current_user = await get_current_user(token=fake_token, db=AsyncMock())

    assert current_user.id == fake_user.id


async def test_get_current_user_invalid(fake_token, mock_repo_get_user_by_id, fake_uuid):
    mock_repo_get_user_by_id.return_value = None
    access_token = AuthUtils.create_access_token({"sub": str(fake_uuid)})
    fake_token = fake_token(access_token)
    with pytest.raises(Unauthorized):
        await get_current_user(token=fake_token, db=AsyncMock())
