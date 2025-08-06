import uuid
from typing import Protocol

from app.db.models import User
from app.schemas import auth as schemas_auth
from app.schemas import users as schemas_users


class IUserService(Protocol):
    async def get_user_by_id(self, user_id: uuid.UUID) -> User: ...
    async def update_user(self, update_data: schemas_users.UserUpdate, user: User) -> User: ...


class IAuthService(Protocol):
    async def register(self, user_data: schemas_users.UserCreate) -> dict: ...
    async def login(self, login_data: schemas_auth.UserLogin) -> dict: ...
    async def change_password(self, pass_data: schemas_auth.PasswordChange, user: User) -> None: ...
