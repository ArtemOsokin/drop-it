import json

import pytest
from app.api.exceptions import auth_exceptions
from app.services.auth import AuthService

@pytest.mark.asyncio
async def test_user_service_without_db(fake_user_create):
    user_service = AuthService()
    with pytest.raises(RuntimeError):
        await user_service.register(user_data=fake_user_create)


@pytest.mark.asyncio
@pytest.mark.usefixtures('apply_migrations')
async def test_register_success(session, fake_user_create):
    auth_service = AuthService(db=session)
    tokens = await auth_service.register(user_data=fake_user_create)
    tokens = json.loads(tokens.model_dump_json())
    assert tokens is not None
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens['token_type'] == 'bearer'


@pytest.mark.asyncio
@pytest.mark.usefixtures('apply_migrations')
async def test_register_username_error(session, fake_user_create, created_user):
    auth_service = AuthService(db=session)
    fake_user_create.username = created_user.username
    with pytest.raises(auth_exceptions.UserAlreadyExistsUsername):
        await auth_service.register(user_data=fake_user_create)



@pytest.mark.asyncio
@pytest.mark.usefixtures('apply_migrations')
async def test_register_email_error(session, fake_user_create, created_user):
    auth_service = AuthService(db=session)
    fake_user_create.email = created_user.email
    with pytest.raises(auth_exceptions.UserAlreadyExistsEmail):
        await auth_service.register(user_data=fake_user_create)