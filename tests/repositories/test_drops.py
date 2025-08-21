import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.core.config import settings
from app.models import Drop

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


async def test_get_drop_by_id(created_drop, drop_repo):
    drop = await drop_repo.get_drop_by_id(created_drop.id)
    assert drop.id == created_drop.id
    assert drop == created_drop


async def test_get_drop_by_id_none(fake_uuid, drop_repo):
    drop = await drop_repo.get_drop_by_id(fake_uuid)
    assert drop is None


async def test_list_drops(drop_creator, drop_repo):
    cnt_drops = 5
    page_size = settings.PAGINATION_DEFAULT_PAGE_SIZE
    created_drops = [await drop_creator(commit=True) for _ in range(cnt_drops)]
    created_ids = [d.id for d in created_drops]

    drops = await drop_repo.list_drops(page=1, page_size=page_size)

    assert len(drops) == cnt_drops
    assert [d.id for d in drops] == list(reversed(created_ids))
    assert len(drops) <= page_size
    for drop in drops:
        assert drop.id in created_ids
        assert drop.created_at is not None
        assert drop.updated_at is not None


async def test_list_drops_none(drop_repo):
    drops = await drop_repo.list_drops(page=1, page_size=settings.PAGINATION_DEFAULT_PAGE_SIZE)

    assert len(drops) == 0
    assert drops == []
    assert not drops


async def test_count_drops(drop_creator, drop_repo):
    cnt_drops = 5
    _ = [await drop_creator(commit=True) for _ in range(cnt_drops)]
    count = await drop_repo.count_drops()

    assert count == cnt_drops


async def test_count_drops_none(drop_repo):
    count = await drop_repo.count_drops()
    assert count == 0
