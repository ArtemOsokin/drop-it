# pylint: disable=unused-argument,too-many-positional-arguments,R0801
import pytest
from fastapi import status

from app.exceptions import user_exceptions
from app.exceptions.error_messages import UserErrorMessage
from app.schemas.users import UserRead

pytestmark = pytest.mark.asyncio


async def test_get_user_success(client, fake_user_with_meta, mock_service_get_user_by_id):
    mock_service_get_user_by_id.return_value = fake_user_with_meta
    response = await client.get(f'v1/users/{str(fake_user_with_meta.id)}')
    assert response.status_code == status.HTTP_200_OK

    user_response = UserRead.model_validate(response.json())

    assert user_response.id == fake_user_with_meta.id
    assert user_response.username == fake_user_with_meta.username


async def test_get_user_not_found(client, fake_uuid, mock_service_get_user_by_id):
    mock_service_get_user_by_id.side_effect = user_exceptions.UserNotFound
    response = await client.get(f'v1/users/{fake_uuid}')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == UserErrorMessage.USER_NOT_FOUND


async def test_update_me_success(
    override_get_current_user,
    client,
    fake_update_user_data,
    fake_token_data,
    fake_user,
    fake_header,
    mock_service_update_user,
):
    mock_service_update_user.return_value = fake_user
    response = await client.patch(
        "v1/users/me",
        headers=fake_header,
        json=fake_update_user_data,
    )
    assert response.status_code == status.HTTP_200_OK

    user = response.json()
    assert user is not None
    assert user['id'] is not None
    assert user['email'] == fake_user.email
    assert user['username'] == fake_user.username


async def test_update_me_username_error(
    override_get_current_user,
    client,
    fake_update_user_data,
    fake_token_data,
    fake_header,
    mock_service_update_user,
):
    mock_service_update_user.side_effect = user_exceptions.UsernameAlreadyExists
    response = await client.patch(
        "v1/users/me",
        headers=fake_header,
        json=fake_update_user_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == UserErrorMessage.USERNAME_ALREADY_EXIST


async def test_update_me_email_error(
    override_get_current_user,
    client,
    fake_update_user_data,
    fake_token_data,
    fake_header,
    mock_service_update_user,
):
    mock_service_update_user.side_effect = user_exceptions.EmailAlreadyExists
    response = await client.patch(
        "v1/users/me",
        headers=fake_header,
        json=fake_update_user_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == UserErrorMessage.EMAIL_ALREADY_EXIST
