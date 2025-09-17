# pylint: disable=unused-argument,too-many-positional-arguments
import datetime as dt

import pytest
from fastapi import status

from app.exceptions import auth_exceptions, drop_exceptions
from app.exceptions.error_messages import AuthErrorMessage, DropErrorMessage
from app.schemas.base import PaginatedResponse
from app.schemas.drops import DropOut

pytestmark = pytest.mark.asyncio


async def test_create_drop_success(
    client,
    fake_drop_data_request,
    fake_user_data,
    fake_genre_data,
    fake_uuid,
    override_get_current_user,
    mock_service_create_drop,
):
    fake_drop_data_response = fake_drop_data_request.copy()

    fake_drop_data_response.update(
        {
            'id': str(fake_uuid),
            'is_expired': False,
            'expires_at': dt.datetime.now().isoformat(),
            'created_at': dt.datetime.now().isoformat(),
            'updated_at': dt.datetime.now().isoformat(),
            "artist": {
                'id': str(fake_uuid),
                'username': fake_user_data['username'],
                'avatar_url': fake_user_data['avatar_url'],
                'is_artist': fake_user_data['is_artist'],
            },
            "genre": {
                'id': str(fake_uuid),
                'name': fake_genre_data['name'],
                'slug': fake_genre_data['slug'],
            },
        }
    )

    mock_service_create_drop.return_value = fake_drop_data_response
    response = await client.post("v1/drops/", json=fake_drop_data_request)

    assert response.status_code == status.HTTP_201_CREATED

    data = response.json()
    assert data['id'] == fake_drop_data_response['id']
    assert data['title'] == fake_drop_data_response['title']
    assert data['genre'] == fake_drop_data_response['genre']
    assert data['artist'] == fake_drop_data_response['artist']


async def test_create_drop_genre_not_found(
    client,
    fake_drop_data_request,
    override_get_current_user,
    mock_service_create_drop,
):

    mock_service_create_drop.side_effect = drop_exceptions.GenreNotFound
    response = await client.post("v1/drops/", json=fake_drop_data_request)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == DropErrorMessage.GENRE_NOT_FOUND


async def test_get_drop_success(
    client, fake_drop, fake_header, mock_service_get_drop_by_id, override_get_current_user
):
    mock_service_get_drop_by_id.return_value = fake_drop
    response = await client.get(f'v1/drops/{str(fake_drop.id)}', headers=fake_header)
    assert response.status_code == status.HTTP_200_OK

    drop_response = DropOut.model_validate(response.json())

    assert drop_response.id == fake_drop.id
    assert drop_response.title == fake_drop.title


async def test_get_drop_not_found(
    client, fake_drop, fake_header, mock_service_get_drop_by_id, override_get_current_user
):
    mock_service_get_drop_by_id.side_effect = drop_exceptions.DropNotFound
    response = await client.get(f'v1/drops/{str(fake_drop.id)}', headers=fake_header)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == DropErrorMessage.DROP_NOT_FOUND


async def test_get_drops_success(
    client, fake_drop, fake_header, mock_service_list_drops, override_get_current_user
):
    cnt_drops = 5
    fake_drops = [fake_drop for _ in range(cnt_drops)]
    fake_drops_ids = [d.id for d in fake_drops]
    mock_service_list_drops.return_value = (fake_drops, cnt_drops)
    response = await client.get('v1/drops/', headers=fake_header)
    assert response.status_code == status.HTTP_200_OK

    drops_response = PaginatedResponse[DropOut].model_validate(response.json())
    assert len(drops_response.items) == cnt_drops
    assert drops_response.total == cnt_drops

    for drop in drops_response.items:
        assert drop.id in fake_drops_ids


async def test_get_drops_none(
    client, fake_header, mock_service_list_drops, override_get_current_user
):
    mock_service_list_drops.return_value = ([], 0)
    response = await client.get('v1/drops/', headers=fake_header)
    assert response.status_code == status.HTTP_200_OK

    drops_response = PaginatedResponse[DropOut].model_validate(response.json())
    assert len(drops_response.items) == 0
    assert drops_response.total == 0
    assert not drops_response.items


async def test_update_drop_success(
    override_get_current_user,
    client,
    fake_drop_update_data,
    fake_drop,
    fake_header,
    mock_service_update_drop,
):
    mock_service_update_drop.return_value = fake_drop
    response = await client.patch(
        f"v1/drops/{fake_drop.id}",
        headers=fake_header,
        json=fake_drop_update_data,
    )
    assert response.status_code == status.HTTP_200_OK

    drop = response.json()
    assert drop is not None
    assert drop['id'] is not None
    assert drop['title'] == fake_drop.title
    assert drop['description'] == fake_drop.description
    assert drop['file_url'] == fake_drop.file_url
    assert drop['genre']['id'] == str(fake_drop.genre_id)


async def test_update_drop_permission_error(
    override_get_current_user,
    client,
    fake_drop_update_data,
    fake_drop,
    fake_header,
    mock_service_update_drop,
):
    mock_service_update_drop.side_effect = auth_exceptions.PermissionDenied
    response = await client.patch(
        f"v1/drops/{fake_drop.id}",
        headers=fake_header,
        json=fake_drop_update_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == AuthErrorMessage.PERMISSION_DENIED


async def test_update_drop_not_found_error(
    override_get_current_user,
    client,
    fake_drop_update_data,
    fake_drop,
    fake_header,
    mock_service_update_drop,
):
    mock_service_update_drop.side_effect = drop_exceptions.DropNotFound
    response = await client.patch(
        f"v1/drops/{fake_drop.id}",
        headers=fake_header,
        json=fake_drop_update_data,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()['error'] == DropErrorMessage.DROP_NOT_FOUND
