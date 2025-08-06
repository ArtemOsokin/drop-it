import uuid

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import get_user_service
from app.api.exceptions import user_exceptions
from app.api.exceptions.error_messages import UserErrorMessage
from app.api.exceptions.http_exceptions import BadRequest
from app.db.models.user import User
from app.schemas import users as schemas_user
from app.services.interfaces import IUserService
from app.services.users import UserService

router = APIRouter()


@router.get(
    path='/{user_id}',
    response_model=schemas_user.UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user by ID",
    description="Get user details by user ID (UUID).",
)
async def get_user(
    user_id: uuid.UUID, user_service: IUserService = Depends(get_user_service)
) -> schemas_user.UserResponse:
    try:
        user = await user_service.get_user_by_id(user_id=user_id)
    except user_exceptions.UserNotFound as e:
        raise BadRequest(enum_error=UserErrorMessage.USER_NOT_FOUND) from e
    return schemas_user.UserResponse.model_validate(user)


@router.patch(
    '/me',
    response_model=schemas_user.UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Update Me",
    description="Update data for current user.",
)
async def update_me(
    update_data: schemas_user.UserUpdate,
    current_user: User = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service),
) -> schemas_user.UserResponse:
    try:
        user = await user_service.update_user(update_data=update_data, user=current_user)
    except user_exceptions.UsernameAlreadyExists as e:
        raise BadRequest(enum_error=UserErrorMessage.USERNAME_ALREADY_EXIST) from e
    except user_exceptions.EmailAlreadyExists as e:
        raise BadRequest(enum_error=UserErrorMessage.EMAIL_ALREADY_EXIST) from e
    return schemas_user.UserResponse.model_validate(user)
