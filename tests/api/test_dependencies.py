import pytest

from app.api.dependencies.auth import get_current_user  # путь адаптируй под себя
from app.api.exceptions.http_exceptions import Unauthorized
from app.core.security import AuthUtils

pytestmark = pytest.mark.asyncio


async def test_get_current_user_valid(monkeypatch, mock_user_repo, fake_token, fake_user_with_meta):
    mock_user_repo.get_user_by_id.return_value = fake_user_with_meta

    async def override_get_user_repository():
        return mock_user_repo

    monkeypatch.setattr(
        'app.api.dependencies.auth.get_user_repository', override_get_user_repository
    )

    access_token = AuthUtils.create_access_token({"sub": str(fake_user_with_meta.id)})
    fake_token_instance = fake_token(access_token)

    user_repo_instance = await override_get_user_repository()

    current_user = await get_current_user(token=fake_token_instance, user_repo=user_repo_instance)

    assert current_user.id == fake_user_with_meta.id

    user_repo_instance.get_user_by_id.assert_awaited_once()


async def test_get_current_user_invalid(monkeypatch, mock_user_repo, fake_token, fake_uuid):

    async def override_get_user_repository():
        return mock_user_repo

    monkeypatch.setattr(
        'app.api.dependencies.auth.get_user_repository', override_get_user_repository
    )

    access_token = AuthUtils.create_access_token({"sub": str(fake_uuid)})
    fake_token_instance = fake_token(access_token)

    user_repo_instance = await override_get_user_repository()

    with pytest.raises(Unauthorized):
        await get_current_user(token=fake_token_instance, user_repo=user_repo_instance)
