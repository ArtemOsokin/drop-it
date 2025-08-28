from unittest.mock import patch

import pytest

from app.admin.views import UserAdmin
from app.core.security import AuthUtils
from app.models import User

pytestmark = pytest.mark.asyncio


async def test_on_model_change_hashes_password():
    user = User()
    data = {"password": "mysecret"}

    admin_view = UserAdmin()

    fake_hashed_password = "hashed_secret"
    with patch.object(AuthUtils, "get_password_hash", return_value=fake_hashed_password):
        await admin_view.on_model_change(data, user, is_created=True, request=None)

    assert user.hashed_password == fake_hashed_password
    assert "password" not in data


async def test_scaffold_form_adds_password_field():
    admin_view = UserAdmin()
    form_class = await admin_view.scaffold_form()

    assert hasattr(form_class, "password")
