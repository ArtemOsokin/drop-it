import pytest
from fastapi import status

from app.api.exceptions import auth_exceptions
from app.api.exceptions.error_messages import AuthErrorMessage, HTTPErrorMessage

pytestmark = pytest.mark.asyncio

async def test_signup_success(
    client, fake_user_data_request, mock_service_register, fake_token_data
):
    mock_service_register.return_value = fake_token_data
    response = await client.post("api/v1/auth/signup", json=fake_user_data_request)

    assert response.status_code == status.HTTP_201_CREATED

    tokens = response.json()
    assert tokens is not None
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens['token_type'] == 'bearer'


async def test_signup_username_error(client, fake_user_data_request, mock_service_register):
    mock_service_register.side_effect = auth_exceptions.UserAlreadyExistsUsername
    response = await client.post("api/v1/auth/signup", json=fake_user_data_request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == AuthErrorMessage.USER_ALREADY_EXIST_USERNAME


async def test_signup_email_error(client, fake_user_data_request, mock_service_register):
    mock_service_register.side_effect = auth_exceptions.UserAlreadyExistsEmail
    response = await client.post("api/v1/auth/signup", json=fake_user_data_request)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == AuthErrorMessage.USER_ALREADY_EXIST_EMAIL


async def test_login_success(mock_service_login, client, fake_login_data, fake_token_data):
    mock_service_login.return_value = fake_token_data
    response = await client.post("api/v1/auth/login", json=fake_login_data)
    assert response.status_code == status.HTTP_200_OK

    tokens = response.json()
    assert tokens is not None
    assert "access_token" in tokens
    assert "refresh_token" in tokens
    assert tokens['token_type'] == 'bearer'


async def test_login_incorrect_username(mock_service_login, client, fake_login_data):
    mock_service_login.side_effect = auth_exceptions.IncorrectUsername
    response = await client.post("api/v1/auth/login", json=fake_login_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == AuthErrorMessage.INCORRECT_USERNAME


@pytest.mark.asyncio
async def test_login_incorrect_password(mock_service_login, client, fake_login_data):
    mock_service_login.side_effect = auth_exceptions.IncorrectPassword
    response = await client.post("api/v1/auth/login", json=fake_login_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == AuthErrorMessage.INCORRECT_PASSWORD


async def test_get_me_success(override_get_current_user, client, fake_token_data, fake_user):
    response = await client.get(
        "api/v1/auth/me", headers={"Authorization": f"Bearer {fake_token_data['access_token']}"}
    )
    assert response.status_code == status.HTTP_200_OK

    user = response.json()
    assert user is not None
    assert user['id'] is not None
    assert user['email'] == fake_user.email
    assert user['username'] == fake_user.username


async def test_get_me_unauthorized_error(
    override_get_current_user_unauthorized, client, fake_token_data
):
    response = await client.get(
        "api/v1/auth/me", headers={"Authorization": f"Bearer {fake_token_data['access_token']}"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json()['error'] == HTTPErrorMessage.USER_UNAUTHORIZED


async def test_change_password_success(
    override_get_current_user,
    mock_service_change_password,
    client,
    fake_token_data,
    fake_user,
    faker,
):
    response = await client.post(
        "api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {fake_token_data['access_token']}"},
        json={
            'current_password': faker.password(),
            'new_password': faker.password(),
        },
    )
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_change_password_error(
    override_get_current_user,
    mock_service_change_password,
    client,
    fake_token_data,
    fake_user,
    faker,
):
    mock_service_change_password.side_effect = auth_exceptions.IncorrectPassword
    response = await client.post(
        "api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {fake_token_data['access_token']}"},
        json={
            'current_password': faker.password(),
            'new_password': faker.password(),
        },
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == AuthErrorMessage.INCORRECT_PASSWORD
