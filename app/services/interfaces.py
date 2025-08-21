import uuid
from typing import Protocol

from app.models import Drop, Genre, User
from app.schemas import auth as schemas_auth
from app.schemas import drops as schemas_drops
from app.schemas import users as schemas_users


class IUserService(Protocol):
    async def get_user_by_id(self, user_id: uuid.UUID) -> User: ...
    async def update_user(self, update_data: schemas_users.UserUpdate, user: User) -> User: ...


class IAuthService(Protocol):
    async def register(self, user_data: schemas_users.UserCreate) -> dict: ...
    async def login(self, login_data: schemas_auth.UserLogin) -> dict: ...
    async def change_password(self, pass_data: schemas_auth.PasswordChange, user: User) -> None: ...


class IDropService(Protocol):
    async def create_drop(
        self, drop_data: schemas_drops.DropCreate, user_id: uuid.UUID
    ) -> Drop: ...
    async def get_drop_by_id(self, drop_id: uuid.UUID) -> Drop: ...
    async def list_genres(self) -> list[Genre]: ...

    async def list_drops(
        self, page: int, page_size: int, genre_id: str, artist_id: str
    ) -> list[Drop]: ...
