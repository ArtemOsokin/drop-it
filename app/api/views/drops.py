from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import get_drop_service
from app.db.models import User
from app.exceptions import drop_exceptions
from app.exceptions.error_messages import DropErrorMessage
from app.exceptions.http_exceptions import BadRequest
from app.schemas import drops as drops_schemas
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
        raise BadRequest(enum_error=DropErrorMessage.GENRE_NOT_FOUND) from e
    return drops_schemas.DropOut.model_validate(drop)
