import json

import pytest
from fastapi import status
from sqlalchemy import select

from app.api.exceptions.error_messages import AuthErrorMessage
from app.db.models import User
from app.schemas.users import UserResponse


@pytest.mark.asyncio
async def test_register(client, fake_user_data, async_session):
    response = await client.post("api/v1/auth/register", json=fake_user_data)

    assert response.status_code == status.HTTP_201_CREATED

    tokens = response.json()
    assert tokens is not None
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens['token_type'] == 'bearer'

    result = await async_session.execute(select(User).where(User.email == fake_user_data['email']))
    db_user = result.scalar_one_or_none()
    assert db_user is not None
    assert db_user.username == fake_user_data['username']


@pytest.mark.asyncio
async def test_register_username_error(client, fake_user_data, created_user):
    fake_user_data['username'] = created_user.username
    response = await client.post("api/v1/auth/register", json=fake_user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == AuthErrorMessage.USER_ALREADY_EXIST_USERNAME



@pytest.mark.asyncio
async def test_register_email_error(client, fake_user_data, created_user):
    fake_user_data['email'] = created_user.email
    response = await client.post("api/v1/auth/register", json=fake_user_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == AuthErrorMessage.USER_ALREADY_EXIST_EMAIL
