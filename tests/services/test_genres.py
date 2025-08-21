from unittest.mock import AsyncMock

import pytest

pytestmark = pytest.mark.asyncio


async def test_list_genres(fake_genre, drop_service):
    cnt_genres = 5
    fake_genres = [fake_genre for _ in range(cnt_genres)]
    drop_service.drop_repo.list_genres = AsyncMock(return_value=fake_genres)
    genres = await drop_service.list_genres()
    assert len(genres) == cnt_genres


async def test_list_genres_none(drop_service):
    drop_service.drop_repo.list_genres = AsyncMock(return_value=[])
    genres = await drop_service.list_genres()
    assert len(genres) == 0
    assert not genres
