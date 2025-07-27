from app.db.models import User
from app.services.base import BaseServiceDB
from app.services.user import UserService


class AuthService(BaseServiceDB):
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def create_user(self, user: User) -> User:
        pass
