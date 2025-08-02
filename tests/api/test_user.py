import pytest
from fastapi import status

from app.api.exceptions.error_messages import UserErrorMessage
from app.schemas.users import UserResponse


@pytest.mark.asyncio
async def test_get_user_success(client, created_user):
    response = await client.get(f'api/v1/users/{created_user.id}')
    assert response.status_code == status.HTTP_200_OK

    user_response = UserResponse.model_validate(response.json())

    assert user_response.id == created_user.id
    assert user_response.username == created_user.username


@pytest.mark.asyncio
async def test_get_user_not_found(client, fake_uuid):
    response = await client.get(f'api/v1/users/{fake_uuid}')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == UserErrorMessage.USER_NOT_FOUND
