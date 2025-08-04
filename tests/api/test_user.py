import pytest
from fastapi import status

from app.api.exceptions import user_exceptions
from app.api.exceptions.error_messages import UserErrorMessage
from app.schemas.users import UserResponse


@pytest.mark.asyncio
async def test_get_user_success(client, fake_user, mock_service_get_user_by_id):
    mock_service_get_user_by_id.return_value = fake_user
    response = await client.get(f'api/v1/users/{str(fake_user.id)}')
    assert response.status_code == status.HTTP_200_OK

    user_response = UserResponse.model_validate(response.json())

    assert user_response.id == fake_user.id
    assert user_response.username == fake_user.username


@pytest.mark.asyncio
async def test_get_user_not_found(client, fake_uuid, mock_service_get_user_by_id):
    mock_service_get_user_by_id.side_effect = user_exceptions.UserNotFound
    response = await client.get(f'api/v1/users/{fake_uuid}')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == UserErrorMessage.USER_NOT_FOUND
