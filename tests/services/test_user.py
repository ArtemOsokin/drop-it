import pytest

from app.api.exceptions.user_exceptions import UserNotFound
from app.services.user import UserService


@pytest.mark.asyncio
@pytest.mark.usefixtures('apply_migrations')
async def test_get_user_by_id(created_user, session):
    user_service = UserService()
    user = await user_service.get_user_by_id(user_id=created_user.id, db=session)
    print(user)
    assert user is not None
    assert user.id == created_user.id


@pytest.mark.asyncio
@pytest.mark.usefixtures('apply_migrations')
async def test_get_user_by_id_not_found(fake_uuid, session):
    user_service = UserService()
    with pytest.raises(UserNotFound):
        await user_service.get_user_by_id(user_id=fake_uuid, db=session)
