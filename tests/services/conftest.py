from unittest.mock import AsyncMock

import pytest

from app.repositories.user import UserRepository


@pytest.fixture
def mock_user_repo_get_user_by_id(mocker):
    return mocker.patch.object(UserRepository, 'get_user_by_id', AsyncMock())
