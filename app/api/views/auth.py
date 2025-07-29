from fastapi import status

from app.api.dependencies.services import get_auth_service
from app.api.exceptions.error_messages import AuthErrorMessage
from app.api.exceptions.http_exceptions import BadRequest
from app.schemas import auth as schemas_auth
from app.schemas import users as schemas_user
from fastapi import APIRouter, Depends

from app.services.auth import AuthService
from app.api.exceptions import auth_exceptions

router = APIRouter(tags=["auth"], prefix="/api/v1/auth")


@router.post(
    path='/register',
    response_model=schemas_auth.Token,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user and return user details."
)
async def register(
    user_data: schemas_user.UserCreate,
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        tokens = await auth_service.register(user_data=user_data)
    except auth_exceptions.UserAlreadyExistsEmail:
        raise BadRequest(enum_error=AuthErrorMessage.USER_ALREADY_EXIST_EMAIL)
    except auth_exceptions.UserAlreadyExistsUsername:
        raise BadRequest(enum_error=AuthErrorMessage.USER_ALREADY_EXIST_USERNAME)
    return tokens
