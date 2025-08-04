import json

import pytest

from app.api.exceptions import auth_exceptions
from app.core.security import AuthUtils
from app.services.auth import AuthService

pytestmark = pytest.mark.asyncio


async def test_user_service_without_db(fake_user_create):
    auth_service = AuthService()
    with pytest.raises(RuntimeError):
        await auth_service.register(user_data=fake_user_create)


async def test_register_success(
    fake_user_create,
    auth_service,
    mock_repo_get_user_by_username,
    mock_repo_get_user_by_email,
    mock_repo_save_user,
    fake_user,
):
    mock_repo_get_user_by_email.return_value = None
    mock_repo_get_user_by_username.return_value = None
    mock_repo_save_user.return_value = fake_user
    tokens = await auth_service.register(user_data=fake_user_create)
    tokens = json.dumps(tokens)
    assert tokens is not None
    assert "access_token" in tokens
    assert "refresh_token" in tokens


async def test_register_username_error(
    fake_user_create,
    fake_user,
    mock_repo_get_user_by_username,
    mock_repo_get_user_by_email,
    auth_service,
):
    mock_repo_get_user_by_username.return_value = fake_user
    mock_repo_get_user_by_email.return_value = None
    with pytest.raises(auth_exceptions.UserAlreadyExistsUsername):
        await auth_service.register(user_data=fake_user_create)


async def test_register_email_error(
    fake_user_create,
    fake_user,
    mock_repo_get_user_by_email,
    mock_repo_get_user_by_username,
    auth_service,
):
    mock_repo_get_user_by_username.return_value = None
    mock_repo_get_user_by_email.return_value = fake_user
    with pytest.raises(auth_exceptions.UserAlreadyExistsEmail):
        await auth_service.register(user_data=fake_user_create)


async def test_login_success(
    auth_service, fake_user_login, mock_repo_get_user_by_username, fake_user
):
    fake_user.username = fake_user_login.username
    fake_user.hashed_password = AuthUtils.get_password_hash(fake_user_login.password)

    mock_repo_get_user_by_username.return_value = fake_user
    tokens = await auth_service.login(login_data=fake_user_login)
    assert tokens is not None
    assert "access_token" in tokens
    assert "refresh_token" in tokens


async def test_login_incorrect_username_error(
    auth_service, fake_user_login, mock_repo_get_user_by_username
):
    mock_repo_get_user_by_username.return_value = None
    with pytest.raises(auth_exceptions.IncorrectUsername):
        await auth_service.login(login_data=fake_user_login)


async def test_login_incorrect_password_error(
    auth_service, fake_user_login, mock_repo_get_user_by_username, fake_user, faker
):
    fake_user.username = fake_user_login.username
    fake_user.hashed_password = AuthUtils.get_password_hash(fake_user_login.password)

    mock_repo_get_user_by_username.return_value = fake_user
    fake_user_login.password = faker.password()
    with pytest.raises(auth_exceptions.IncorrectPassword):
        await auth_service.login(login_data=fake_user_login)
