import pytest
from sqlalchemy import select

from app.db.models import User

pytestmark = pytest.mark.asyncio

async def test_get_user_by_id(created_user, async_session, user_repo):
    user = await user_repo.get_user_by_id(created_user.id)
    print(user)
    assert user.id == created_user.id
    assert user == created_user


async def test_get_user_by_id_none(async_session, fake_uuid, user_repo):
    user = await user_repo.get_user_by_id(fake_uuid)
    assert user is None


async def test_get_user_by_username(created_user, async_session, user_repo):
    user = await user_repo.get_user_by_username(created_user.username)
    assert user.username == created_user.username
    assert user.id == created_user.id
    assert user == created_user


async def test_get_user_by_username_none(async_session, faker, user_repo):
    user = user_repo.get_user_by_username(faker.user_name())
    assert user is None


async def test_get_user_by_email(created_user, async_session, user_repo):
    user = await user_repo.get_user_by_email(created_user.email)
    assert user.email == created_user.email
    assert user.id == created_user.id
    assert user == created_user


async def test_get_user_by_email_none(async_session, faker, user_repo):
    user = await user_repo.get_user_by_email(faker.email())
    assert user is None

async def test_create_user(async_session, fake_user, user_repo):
    user = await user_repo.create_user(fake_user)
    assert user is not None
    assert user.id is not None
    assert user.email == fake_user.email
    assert user.username == fake_user.username

    assert user.created_at is not None
    assert user.updated_at is not None

    result = await async_session.execute(select(User).where(User.email == fake_user.email))
    db_user = result.scalar_one_or_none()
    assert db_user is not None
    assert db_user.id == user.id
