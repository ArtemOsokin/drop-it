import pytest
from sqlalchemy import select

from app.models.user import User

pytestmark = [pytest.mark.asyncio, pytest.mark.usefixtures('apply_migrations', 'clean_tables')]


async def test_get_user_by_id(created_user, user_repo):
    user = await user_repo.get_user_by_id(created_user.id)
    assert user.id == created_user.id
    assert user == created_user


async def test_get_user_by_id_none(fake_uuid, user_repo):
    user = await user_repo.get_user_by_id(fake_uuid)
    assert user is None


async def test_get_user_by_username(created_user, user_repo):
    user = await user_repo.get_user_by_username(created_user.username)
    assert user.username == created_user.username
    assert user.id == created_user.id
    assert user == created_user


async def test_get_user_by_username_none(faker, user_repo):
    user = await user_repo.get_user_by_username(faker.user_name())  # Добавлен await!
    assert user is None


async def test_get_user_by_email(created_user, user_repo):
    user = await user_repo.get_user_by_email(created_user.email)
    assert user.email == created_user.email
    assert user.id == created_user.id
    assert user == created_user


async def test_get_user_by_email_none(faker, user_repo):
    user = await user_repo.get_user_by_email(faker.email())
    assert user is None


async def test_save_user(session, fake_user, user_repo):
    user = await user_repo.save_user(fake_user)
    assert user is not None
    assert user.id is not None
    assert user.email == fake_user.email
    assert user.username == fake_user.username

    assert user.created_at is not None
    assert user.updated_at is not None

    result = await session.execute(select(User).where(User.email == fake_user.email))
    db_user = result.scalar_one_or_none()
    assert db_user is not None
    assert db_user.id == user.id


async def test_save_user_duplicate_email(created_user, fake_user_data, user_repo):
    duplicate_user_data = fake_user_data.copy()
    duplicate_user_data['email'] = created_user.email
    duplicate_user_data['hashed_password'] = duplicate_user_data.pop('password')
    duplicate_user = User(**duplicate_user_data)

    with pytest.raises(Exception):
        await user_repo.save_user(duplicate_user)


async def test_save_user_duplicate_username(created_user, fake_user_data, user_repo):
    duplicate_user_data = fake_user_data.copy()
    duplicate_user_data['username'] = created_user.username
    duplicate_user_data['hashed_password'] = duplicate_user_data.pop('password')
    duplicate_user = User(**duplicate_user_data)

    with pytest.raises(Exception):
        await user_repo.save_user(duplicate_user)
