from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import get_async_session
from app.exceptions.error_messages import HTTPErrorMessage
from app.exceptions.http_exceptions import ServiceUnavailableError

router = APIRouter()


@router.get("/healthz", summary="Health check endpoint")
async def health_check(response: Response, session: AsyncSession = Depends(get_async_session)):
    """
    Проверяет доступность базы данных.
    Возвращает 200 если БД доступна, иначе 503.
    """
    try:
        await session.execute(text("SELECT 1"))
        return {"status": "ok"}
    except (OperationalError, ConnectionRefusedError):
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return ServiceUnavailableError(enum_error=HTTPErrorMessage.DB_UNAVAILABLE)
