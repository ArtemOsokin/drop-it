import pytest
from fastapi import status

from app.schemas.drops import GenreOut

pytestmark = pytest.mark.asyncio


async def test_get_genres_success(
    client,
    fake_genre,
    fake_header,
    mock_service_list_genres,
    override_get_current_user,  # pylint: disable=unused-argument
):
    cnt_genres = 5
    fake_genres = [fake_genre for _ in range(cnt_genres)]
    fake_genres_ids = [d.id for d in fake_genres]
    mock_service_list_genres.return_value = fake_genres
    response = await client.get('v1/genres/', headers=fake_header)
    assert response.status_code == status.HTTP_200_OK

    drops_response = [GenreOut.model_validate(genre) for genre in response.json()]
    assert len(drops_response) == cnt_genres

    for drop in drops_response:
        assert drop.id in fake_genres_ids


async def test_get_genres_none(
    client,
    fake_header,
    mock_service_list_genres,
    override_get_current_user,  # pylint: disable=unused-argument
):
    mock_service_list_genres.return_value = []
    response = await client.get('v1/genres/', headers=fake_header)
    assert response.status_code == status.HTTP_200_OK

    assert len(response.json()) == 0
    assert not response.json()
