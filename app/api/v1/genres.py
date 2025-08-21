from typing import List

from fastapi import APIRouter, Depends, status

from app.api.dependencies.auth import get_current_user
from app.api.dependencies.services import get_drop_service
from app.models import User
from app.schemas import drops as drops_schemas
from app.services.interfaces import IDropService

router = APIRouter()


@router.get(
    path='/',
    response_model=List[drops_schemas.GenreOut],
    status_code=status.HTTP_200_OK,
    summary="Get genres",
    description="Get paginated list genres.",
)
async def get_genres(
    _: User = Depends(get_current_user),
    drop_service: IDropService = Depends(get_drop_service),
):
    genres = await drop_service.list_genres()

    return [drops_schemas.GenreOut.model_validate(genre) for genre in genres]
