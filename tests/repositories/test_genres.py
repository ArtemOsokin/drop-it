import pytest

pytestmark = [pytest.mark.asyncio, pytest.mark.usefixtures('apply_migrations', 'clean_tables')]


async def test_get_genre_by_id(created_genre, drop_repo):
    genre = await drop_repo.get_genre_by_id(created_genre.id)
    assert genre.id == created_genre.id
    assert genre == created_genre


async def test_get_genre_by_id_none(fake_uuid, drop_repo):
    genre = await drop_repo.get_genre_by_id(fake_uuid)
    assert genre is None


async def test_list_genres(genre_creator, drop_repo):
    cnt_genres = 5
    created_genres = [await genre_creator(commit=True) for _ in range(cnt_genres)]
    created_ids = [d.id for d in created_genres]

    genres = await drop_repo.list_genres()

    assert len(genres) == cnt_genres
    for drop in genres:
        assert drop.id in created_ids
        assert drop.created_at is not None
        assert drop.updated_at is not None


async def test_list_genres_none(drop_repo):
    genres = await drop_repo.list_genres()

    assert len(genres) == 0
    assert genres == []
    assert not genres
