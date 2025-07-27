import pytest

from app.repositories.user import UserRepository


@pytest.mark.usefixtures('apply_migrations')
def test_get_user_by_id(created_user, session):
    user_repo = UserRepository(db=session)
    user = user_repo.get_user_by_id(created_user.id)
    assert user.id == created_user.id
    assert user == created_user


@pytest.mark.usefixtures('apply_migrations')
def test_get_user_by_id_none(session, fake_uuid):
    user_repo = UserRepository(db=session)
    user = user_repo.get_user_by_id(fake_uuid)
    assert user is None
