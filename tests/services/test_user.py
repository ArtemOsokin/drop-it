import pytest

from app.api.exceptions.user_exceptions import UserNotFound
from app.services.user import UserService

pytestmark = pytest.mark.asyncio

async def test_user_service_without_db(fake_uuid):
    user_service = UserService()
    with pytest.raises(RuntimeError):
        await user_service.get_user_by_id(user_id=fake_uuid)


async def test_get_user_by_id(created_user, async_session):
    user_service = UserService(db=async_session)
    user = await user_service.get_user_by_id(user_id=created_user.id)
    assert user is not None
    assert user.id == created_user.id


async def test_get_user_by_id_not_found(fake_uuid, async_session):
    if hasattr(async_session, "__anext__"):
        raise ValueError('Not Acync session')
    user_service = UserService(db=async_session)
    with pytest.raises(UserNotFound):
        await user_service.get_user_by_id(user_id=fake_uuid)
