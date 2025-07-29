import pytest

from app.db.models import User


@pytest.mark.usefixtures('apply_migrations')
def test_get_user_by_id(created_user, session, user_repo):
    user = user_repo.get_user_by_id(created_user.id)
    assert user.id == created_user.id
    assert user == created_user


@pytest.mark.usefixtures('apply_migrations')
def test_get_user_by_id_none(session, fake_uuid, user_repo):
    user = user_repo.get_user_by_id(fake_uuid)
    assert user is None


@pytest.mark.usefixtures('apply_migrations')
def test_get_user_by_username(created_user, session, user_repo):
    user = user_repo.get_user_by_username(created_user.username)
    assert user.username == created_user.username
    assert user.id == created_user.id
    assert user == created_user


@pytest.mark.usefixtures('apply_migrations')
def test_get_user_by_username_none(session, faker, user_repo):
    user = user_repo.get_user_by_username(faker.user_name())
    assert user is None


@pytest.mark.usefixtures('apply_migrations')
def test_get_user_by_email(created_user, session, user_repo):
    user = user_repo.get_user_by_email(created_user.email)
    assert user.email == created_user.email
    assert user.id == created_user.id
    assert user == created_user


@pytest.mark.usefixtures('apply_migrations')
def test_get_user_by_email_none(session, faker, user_repo):
    user = user_repo.get_user_by_email(faker.email())
    assert user is None

@pytest.mark.usefixtures('apply_migrations')
def test_create_user(session, fake_user, user_repo):
    user = user_repo.create_user(fake_user)
    assert user is not None
    assert user.id is not None
    assert user.email == fake_user.email
    assert user.username == fake_user.username

    assert user.created_at is not None
    assert user.updated_at is not None

    db_user = session.query(User).filter(User.email == fake_user.email).first()
    assert db_user is not None
    assert db_user.id == user.id
