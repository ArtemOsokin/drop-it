# pylint: disable=unused-argument,too-many-positional-arguments
from unittest.mock import AsyncMock

import pytest

from app.core.config import settings
from app.exceptions import auth_exceptions, drop_exceptions

pytestmark = pytest.mark.asyncio


async def test_create_drop_success(
    fake_drop_create, drop_service, fake_genre, fake_user, fake_drop, fake_uuid
):
    fake_genre.id = fake_uuid
    drop_service.drop_repo.get_genre_by_id.return_value = fake_genre
    drop_service.drop_repo.save_drop.return_value = fake_drop
    drop = await drop_service.create_drop(drop_data=fake_drop_create, user_id=fake_user.id)
    assert drop is not None
    assert drop.id == fake_drop.id
    assert drop.title == fake_drop.title
    drop_service.drop_repo.get_genre_by_id.assert_awaited_once_with(fake_genre.id)
    drop_service.drop_repo.save_drop.assert_awaited_once()


async def test_create_drop_genre_not_found(fake_drop_create, drop_service, fake_user):
    drop_service.drop_repo.get_genre_by_id.return_value = None
    with pytest.raises(drop_exceptions.GenreNotFound):
        await drop_service.create_drop(drop_data=fake_drop_create, user_id=fake_user.id)


async def test_get_drop_by_id_success(fake_drop, drop_service):
    drop_service.drop_repo.get_drop_by_id.return_value = fake_drop
    drop = await drop_service.get_drop_by_id(drop_id=fake_drop.id)
    assert drop is not None
    assert drop.id == fake_drop.id


async def test_get_drop_by_id_not_found(fake_drop, drop_service):
    drop_service.drop_repo.get_drop_by_id.return_value = None
    with pytest.raises(drop_exceptions.DropNotFound):
        await drop_service.get_drop_by_id(drop_id=fake_drop.id)


async def test_list_drops(fake_drop, drop_service):
    cnt_drops = 5
    fake_drops = [fake_drop for _ in range(cnt_drops)]
    drop_service.drop_repo.list_drops = AsyncMock(return_value=fake_drops)
    drop_service.drop_repo.count_drops.return_value = cnt_drops
    drops, total = await drop_service.list_drops(
        page=1, page_size=settings.PAGINATION_DEFAULT_PAGE_SIZE
    )
    assert len(drops) == cnt_drops
    assert total == cnt_drops


async def test_list_drops_none(drop_service):
    drop_service.drop_repo.list_drops = AsyncMock(return_value=[])
    drop_service.drop_repo.count_drops.return_value = 0
    drops, total = await drop_service.list_drops(
        page=1, page_size=settings.PAGINATION_DEFAULT_PAGE_SIZE
    )
    assert len(drops) == 0
    assert total == 0
    assert not drops


async def test_update_drop_success(
    fake_drop,
    fake_drop_update,
    drop_service,
):
    drop_service.drop_repo.get_drop_by_id.return_value = fake_drop
    drop_service.drop_repo.save_drop.return_value = fake_drop
    drop = await drop_service.update_drop(
        drop_data=fake_drop_update, drop_id=fake_drop.id, user=fake_drop.artist
    )

    assert drop is not None
    assert drop.title == fake_drop_update.title
    assert drop.description == fake_drop_update.description
    assert drop.cover_url == str(fake_drop_update.cover_url)
    assert drop.file_url == str(fake_drop_update.file_url)


async def test_update_user_drop_not_found_error(
    fake_drop,
    fake_drop_update,
    drop_service,
):
    drop_service.drop_repo.get_drop_by_id.return_value = None
    with pytest.raises(drop_exceptions.DropNotFound):
        await drop_service.update_drop(
            drop_data=fake_drop_update, drop_id=fake_drop.id, user=fake_drop.artist
        )


async def test_update_user_permission_denied_error(
    fake_uuid,
    fake_drop,
    fake_user,
    fake_drop_update,
    drop_service,
):
    drop_service.drop_repo.get_drop_by_id.return_value = fake_drop
    fake_user.is_admin = False
    fake_user.id = fake_uuid
    with pytest.raises(auth_exceptions.PermissionDenied):
        await drop_service.update_drop(
            drop_data=fake_drop_update, drop_id=fake_drop.id, user=fake_user
        )
