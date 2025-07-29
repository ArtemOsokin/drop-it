import pytest

from app.api.exceptions.user_exceptions import UserNotFound
from app.services.user import UserService


@pytest.mark.asyncio
async def test_user_service_without_db(fake_uuid):
    user_service = UserService()
    with pytest.raises(RuntimeError):
        await user_service.get_user_by_id(user_id=fake_uuid)


@pytest.mark.asyncio
@pytest.mark.usefixtures('apply_migrations')
async def test_get_user_by_id(created_user, session):
    user_service = UserService(db=session)
    user = await user_service.get_user_by_id(user_id=created_user.id)
    assert user is not None
    assert user.id == created_user.id


@pytest.mark.asyncio
@pytest.mark.usefixtures('apply_migrations')
async def test_get_user_by_id_not_found(fake_uuid, session):
    user_service = UserService(db=session)
    with pytest.raises(UserNotFound):
        await user_service.get_user_by_id(user_id=fake_uuid)
