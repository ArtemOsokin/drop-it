import json

import pytest

from app.core.security import AuthUtils
from app.exceptions import auth_exceptions

pytestmark = pytest.mark.asyncio


async def test_register_success(
    fake_user_create,
    auth_service,
    fake_user,
):
    auth_service.user_repo.get_user_by_email.return_value = None
    auth_service.user_repo.get_user_by_username.return_value = None
    auth_service.user_repo.save_user.return_value = fake_user
    user, tokens = await auth_service.register(user_data=fake_user_create)
    tokens = json.dumps(tokens)
    assert tokens is not None
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert user.id == fake_user.id
    assert user.email == fake_user.email
    assert user.username == fake_user.username


async def test_register_username_error(
    fake_user_create,
    fake_user,
    auth_service,
):
    auth_service.user_repo.get_user_by_username.return_value = fake_user
    auth_service.user_repo.get_user_by_email.return_value = None
    with pytest.raises(auth_exceptions.UserAlreadyExistsUsername):
        await auth_service.register(user_data=fake_user_create)


async def test_register_email_error(
    fake_user_create,
    fake_user,
    auth_service,
):
    auth_service.user_repo.get_user_by_username.return_value = None
    auth_service.user_repo.get_user_by_email.return_value = fake_user
    with pytest.raises(auth_exceptions.UserAlreadyExistsEmail):
        await auth_service.register(user_data=fake_user_create)


async def test_login_success(auth_service, fake_user_login, fake_user):
    fake_user.username = fake_user_login.username
    fake_user.hashed_password = AuthUtils.get_password_hash(fake_user_login.password)

    auth_service.user_repo.get_user_by_username.return_value = fake_user
    tokens = await auth_service.login(login_data=fake_user_login)
    auth_service.user_repo.get_user_by_username.assert_awaited_once_with(
        username=fake_user_login.username
    )
    assert tokens is not None
    assert "access_token" in tokens
    assert "refresh_token" in tokens


async def test_login_incorrect_username_error(auth_service, fake_user_login):
    auth_service.user_repo.get_user_by_username.return_value = None
    with pytest.raises(auth_exceptions.IncorrectUsername):
        await auth_service.login(login_data=fake_user_login)
    auth_service.user_repo.get_user_by_username.assert_awaited_once_with(
        username=fake_user_login.username
    )


async def test_login_incorrect_password_error(auth_service, fake_user_login, fake_user, faker):
    fake_user.username = fake_user_login.username
    fake_user.hashed_password = AuthUtils.get_password_hash(fake_user_login.password)

    auth_service.user_repo.get_user_by_username.return_value = fake_user
    fake_user_login.password = faker.password()
    with pytest.raises(auth_exceptions.IncorrectPassword):
        await auth_service.login(login_data=fake_user_login)
    auth_service.user_repo.get_user_by_username.assert_awaited_once_with(
        username=fake_user_login.username
    )


async def test_login_admin_success(auth_service, fake_user_login, fake_user):
    fake_user.is_admin = True
    fake_user.username = fake_user_login.username
    fake_user.hashed_password = AuthUtils.get_password_hash(fake_user_login.password)

    auth_service.user_repo.get_admin_by_username.return_value = fake_user
    user = await auth_service.login_admin(
        username=fake_user_login.username, password=fake_user_login.password
    )
    auth_service.user_repo.get_admin_by_username.assert_awaited_once_with(
        username=fake_user_login.username
    )
    assert user is not None
    assert user.username == fake_user.username
    assert user.is_admin
    assert user.email == fake_user.email


async def test_login_admin_incorrect_username_error(auth_service, fake_user_login):
    auth_service.user_repo.get_admin_by_username.return_value = None
    with pytest.raises(auth_exceptions.IncorrectUsername):
        await auth_service.login_admin(
            username=fake_user_login.username, password=fake_user_login.password
        )
    auth_service.user_repo.get_admin_by_username.assert_awaited_once_with(
        username=fake_user_login.username
    )


async def test_login_incorrect_admin_password_error(
    auth_service, fake_user_login, fake_user, faker
):
    fake_user.username = fake_user_login.username
    fake_user.hashed_password = AuthUtils.get_password_hash(fake_user_login.password)

    auth_service.user_repo.get_admin_by_username.return_value = fake_user
    fake_user_login.password = faker.password()
    with pytest.raises(auth_exceptions.IncorrectPassword):
        await auth_service.login_admin(
            username=fake_user_login.username, password=fake_user_login.password
        )
    auth_service.user_repo.get_admin_by_username.assert_awaited_once_with(
        username=fake_user_login.username
    )


async def test_change_password_success(auth_service, fake_change_password, fake_user):
    fake_user.hashed_password = AuthUtils.get_password_hash(fake_change_password.current_password)
    auth_service.user_repo.save_user.return_value = fake_user
    await auth_service.change_password(pass_data=fake_change_password, user=fake_user)
    auth_service.user_repo.save_user.assert_awaited_once()


async def test_change_password_incorrect_password_error(
    auth_service, fake_change_password, fake_user
):
    fake_user.hashed_password = AuthUtils.get_password_hash(fake_user.hashed_password)
    with pytest.raises(auth_exceptions.IncorrectPassword):
        await auth_service.change_password(pass_data=fake_change_password, user=fake_user)
    auth_service.user_repo.save_user.assert_not_awaited()
