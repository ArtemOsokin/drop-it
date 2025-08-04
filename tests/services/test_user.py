import pytest

from app.api.exceptions.user_exceptions import UserNotFound
from app.services.user import UserService

pytestmark = pytest.mark.asyncio


async def test_user_service_without_db(fake_uuid, user_service):
    user_service = UserService()
    with pytest.raises(RuntimeError):
        await user_service.get_user_by_id(user_id=fake_uuid)


async def test_get_user_by_id(mock_repo_get_user_by_id, fake_user, user_service):
    mock_repo_get_user_by_id.return_value = fake_user
    user = await user_service.get_user_by_id(user_id=fake_user.id)
    assert user is not None
    assert user.id == fake_user.id


async def test_get_user_by_id_not_found(fake_uuid, mock_repo_get_user_by_id, user_service):
    mock_repo_get_user_by_id.return_value = None
    with pytest.raises(UserNotFound):
        await user_service.get_user_by_id(user_id=fake_uuid)
