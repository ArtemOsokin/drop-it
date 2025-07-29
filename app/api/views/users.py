import logging
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as SessionType

from app.api.dependencies.services import get_user_service
from app.api.exceptions import user_exceptions
from app.api.exceptions.error_messages import UserErrorMessage
from app.api.exceptions.http_exceptions import BadRequest
from app.db.engine import get_db
from app.schemas import users as schemas_user
from app.services.user import UserService

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
logger.setLevel(logging.INFO)

router = APIRouter(tags=["users"], prefix="/api/v1/users")


@router.get('/{user_id}')
async def get_user(
    user_id: uuid.UUID, user_service: UserService = Depends(get_user_service)
) -> schemas_user.UserResponse:
    try:
        user = await user_service.get_user_by_id(user_id=user_id)
    except user_exceptions.UserNotFound as e:
        raise BadRequest(enum_error=UserErrorMessage.USER_NOT_FOUND) from e
    return schemas_user.UserResponse.model_validate(user)