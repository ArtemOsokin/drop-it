import pytest

from app.api.dependencies.auth import get_current_user  # путь адаптируй под себя
from app.core.security import AuthUtils


class FakeToken:
    """Заменяет HTTPAuthorizationCredentials"""

    def __init__(self, token: str):
        self.credentials = token


@pytest.mark.asyncio
async def test_get_current_user_valid(session, created_user):

    access_token = AuthUtils.create_access_token({"sub": str(created_user.id)})
    fake_token = FakeToken(access_token)
    current_user = await get_current_user(token=fake_token, db=session)

    assert current_user.id == created_user.id
