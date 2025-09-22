import uuid

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import get_drop_service
from app.core.config import settings
from app.exceptions import auth_exceptions, drop_exceptions
from app.exceptions.error_messages import AuthErrorMessage, DropErrorMessage
from app.exceptions.http_exceptions import AccessForbidden, NotFound
from app.models import User
from app.schemas import drops as drops_schemas
from app.schemas.base import PaginatedResponse
from app.services.interfaces import IDropService

router = APIRouter()


@router.post(
    path='/',
    response_model=drops_schemas.DropOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new drop",
    description="Create a new drop and return drop details.",
)
async def create_drop(
    drop_data: drops_schemas.DropCreate,
    current_user: User = Depends(get_current_user),
    drop_service: IDropService = Depends(get_drop_service),
):
    try:
        drop = await drop_service.create_drop(drop_data=drop_data, user_id=current_user.id)
    except drop_exceptions.GenreNotFound as e:
        raise NotFound(enum_error=DropErrorMessage.GENRE_NOT_FOUND) from e
    return drops_schemas.DropOut.model_validate(drop)


@router.get(
    path='/{drop_id}',
    response_model=drops_schemas.DropOut,
    status_code=status.HTTP_200_OK,
    summary="Get drop by id",
    description="Get a drop and return drop details.",
)
async def get_drop_by_id(
    drop_id: uuid.UUID,
    drop_service: IDropService = Depends(get_drop_service),
):
    try:
        drop = await drop_service.get_drop_by_id(drop_id=drop_id)
    except drop_exceptions.DropNotFound as e:
        raise NotFound(enum_error=DropErrorMessage.DROP_NOT_FOUND) from e
    return drops_schemas.DropOut.model_validate(drop)


@router.get(
    path='/',
    response_model=PaginatedResponse[drops_schemas.DropOut],
    status_code=status.HTTP_200_OK,
    summary="Get drops",
    description="Get paginated list drops by filters.",
)
async def get_drops(
    page: int = 1,
    page_size: int = settings.PAGINATION_DEFAULT_PAGE_SIZE,
    genre_id: str = None,
    artist_id: str = None,
    drop_service: IDropService = Depends(get_drop_service),
):
    drops, total = await drop_service.list_drops(
        page=page,
        page_size=page_size,
        genre_id=genre_id,
        artist_id=artist_id,
    )
    return PaginatedResponse(items=drops, total=total, page=page, page_size=page_size)


@router.patch(
    '/{drop_id}',
    response_model=drops_schemas.DropOut,
    status_code=status.HTTP_200_OK,
    summary="Update Drop",
    description="Update data for drop by id.",
)
async def update_drop(
    drop_id: uuid.UUID,
    update_data: drops_schemas.DropUpdate,
    user: User = Depends(get_current_user),
    drop_service: IDropService = Depends(get_drop_service),
):
    try:
        drop = await drop_service.update_drop(drop_data=update_data, drop_id=drop_id, user=user)
    except auth_exceptions.PermissionDenied as e:
        raise AccessForbidden(enum_error=AuthErrorMessage.PERMISSION_DENIED) from e
    except drop_exceptions.DropNotFound as e:
        raise NotFound(enum_error=DropErrorMessage.DROP_NOT_FOUND) from e
    return drops_schemas.DropOut.model_validate(drop)


@router.delete(
    '/{drop_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Drop",
    description="Delete drop by id.",
)
async def delete_drop(
    drop_id: uuid.UUID,
    user: User = Depends(get_current_user),
    drop_service: IDropService = Depends(get_drop_service),
):
    try:
        await drop_service.delete_drop(drop_id=drop_id, user=user)
    except auth_exceptions.PermissionDenied as e:
        raise AccessForbidden(enum_error=AuthErrorMessage.PERMISSION_DENIED) from e
    except drop_exceptions.DropNotFound as e:
        raise NotFound(enum_error=DropErrorMessage.DROP_NOT_FOUND) from e
    return status.HTTP_204_NO_CONTENT
