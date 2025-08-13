import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.db.models import Drop

pytestmark = [pytest.mark.asyncio, pytest.mark.usefixtures('apply_migrations', 'clean_tables')]


async def test_save_drop(session, fake_drop_data_generator, created_user, created_genre, drop_repo):
    fake_drop_data = fake_drop_data_generator(genre_id=created_genre.id, artist_id=created_user.id)
    fake_drop = Drop(**fake_drop_data)
    drop = await drop_repo.save_drop(fake_drop)
    assert drop is not None
    assert drop.id is not None
    assert drop.genre_id == fake_drop.genre_id
    assert drop.artist_id == fake_drop.artist_id

    assert drop.created_at is not None
    assert drop.updated_at is not None

    result = await session.execute(
        select(Drop)
        .options(selectinload(Drop.genre), selectinload(Drop.artist))
        .where(Drop.title == fake_drop.title, Drop.genre_id == created_genre.id)
    )
    db_drop = result.scalar_one_or_none()
    assert db_drop is not None
    assert db_drop.id == drop.id
    assert db_drop.genre.id == created_genre.id
    assert db_drop.artist.id == created_user.id


async def test_get_genre_by_id(created_genre, drop_repo):
    genre = await drop_repo.get_genre_by_id(created_genre.id)
    assert genre.id == created_genre.id
    assert genre == created_genre


async def test_get_user_by_id_none(fake_uuid, drop_repo):
    genre = await drop_repo.get_genre_by_id(fake_uuid)
    assert genre is None
