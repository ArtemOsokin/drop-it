import pytest

from app.schemas.users import UserCreate

@pytest.fixture
def fake_user_create(fake_user_data):
    return UserCreate(**fake_user_data)
