import pytest

from app.api.exceptions import drop_exceptions

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
