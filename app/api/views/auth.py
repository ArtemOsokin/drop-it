from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import get_auth_service
from app.api.exceptions import auth_exceptions, http_exceptions
from app.api.exceptions.error_messages import AuthErrorMessage, HTTPErrorMessage
from app.api.exceptions.http_exceptions import BadRequest
from app.db.models import User
from app.schemas import auth as schemas_auth
from app.schemas import users as schemas_user
from app.services.auth import AuthService

router = APIRouter(tags=["auth"], prefix="/api/v1/auth")


@router.post(
    path='/signup',
    response_model=schemas_auth.Token,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user and return user details.",
)
async def signup(
    user_data: schemas_user.UserCreate, auth_service: AuthService = Depends(get_auth_service)
):
    try:
        tokens = await auth_service.register(user_data=user_data)
    except auth_exceptions.UserAlreadyExistsEmail:
        raise BadRequest(enum_error=AuthErrorMessage.USER_ALREADY_EXIST_EMAIL)
    except auth_exceptions.UserAlreadyExistsUsername:
        raise BadRequest(enum_error=AuthErrorMessage.USER_ALREADY_EXIST_USERNAME)
    return tokens


@router.get(
    path='/me',
    response_model=schemas_user.UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Information about current user",
    description="Information about current user.",
)
async def get_me(current_user: User = Depends(get_current_user)):
    try:
        return schemas_user.UserResponse.model_validate(current_user)
    except http_exceptions.Unauthorized:
        raise BadRequest(enum_error=HTTPErrorMessage.USER_UNAUTHORIZED)
