import pytest

from app.api.exceptions import user_exceptions
from app.api.exceptions.user_exceptions import UserNotFound
from app.db.models import User
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


async def test_update_user_success(
    mock_repo_save_user,
    mock_repo_get_user_by_username,
    mock_repo_get_user_by_email,
    fake_user,
    fake_user_update,
    user_service,
):
    mock_repo_get_user_by_email.return_value = None
    mock_repo_get_user_by_username.return_value = None
    mock_repo_save_user.return_value = User(
        email=fake_user_update.email,
        username=fake_user_update.username,
        avatar_url=fake_user_update.avatar_url,
        first_name=fake_user_update.first_name,
        last_name=fake_user_update.last_name,
        birthday=fake_user_update.birthday,
        is_artist=fake_user_update.is_artist,
    )

    user = await user_service.update_user(update_data=fake_user_update, user=fake_user)
    assert user is not None
    assert user.username == fake_user.username
    assert user.email == fake_user_update.email
    assert user.avatar_url == fake_user_update.avatar_url
    assert user.first_name == fake_user_update.first_name
    assert user.last_name == fake_user_update.last_name
    assert user.birthday == fake_user_update.birthday


async def test_update_user_username_error(
    mock_repo_get_user_by_username,
    mock_repo_get_user_by_email,
    fake_user,
    fake_user_update,
    user_service,
):
    mock_repo_get_user_by_email.return_value = None
    mock_repo_get_user_by_username.return_value = fake_user
    with pytest.raises(user_exceptions.UsernameAlreadyExists):
        await user_service.update_user(update_data=fake_user_update, user=fake_user)


async def test_update_user_email_error(
    mock_repo_get_user_by_username,
    mock_repo_get_user_by_email,
    fake_user,
    fake_user_update,
    user_service,
):
    mock_repo_get_user_by_email.return_value = fake_user
    mock_repo_get_user_by_username.return_value = None
    with pytest.raises(user_exceptions.EmailAlreadyExists):
        await user_service.update_user(update_data=fake_user_update, user=fake_user)
