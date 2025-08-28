from fastapi import Depends
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.db.engine import async_session

from app.core.config import settings
from app.db.repositories.users import UserRepository
from app.exceptions import auth_exceptions
from app.services.auth import AuthService


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:

        form = await request.form()
        username, password = form["username"], form["password"]
        async with async_session() as db:
            auth_service = AuthService(user_repo=UserRepository(db=db))
            try:
                user = await auth_service.login_admin(username, password)
            except (auth_exceptions.IncorrectUsername, auth_exceptions.IncorrectPassword):
                return False

        if not user:
            return False

        request.session.update({"admin_id": str(user.id)})
        return True


    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request):
        if "admin_id" in request.session:
            return True
        return RedirectResponse(request.url_for("admin:login"), status_code=302)


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
