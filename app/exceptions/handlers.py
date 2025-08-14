from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError, IntegrityError
from loguru import logger

from app.exceptions.error_messages import HTTPErrorMessage
from app.exceptions.http_exceptions import BadRequest, BaseApiException


async def handle_exception_response(
    request: Request,
    exc: BaseApiException,
):  # pylint: disable=unused-argument  # pragma: no cover
    return exc.get_response_data()


async def handle_validation_error_handler(
    request: Request,
    exc: RequestValidationError,
):  # pylint: disable=unused-argument  # pragma: no cover
    param_name_index = -1
    all_errors = exc.errors()
    verbose_errors = ', '.join(
        [param_name for param_name in error['loc'] if isinstance(param_name, str)][param_name_index]
        + ' '
        + error['msg']
        for error in all_errors
    )
    error = BadRequest(
        enum_error=HTTPErrorMessage.INCORRECT_DATA,
        verbose_errors=verbose_errors,
    ).get_response_data()

    return error


async def operational_error_handler(request: Request, exc: OperationalError):
    logger.error(f"DB connection error: {exc}")
    return JSONResponse(
        status_code=503,
        content={"detail": "Database temporarily unavailable"}
    )

async def integrity_error_handler(request: Request, exc: IntegrityError):
    logger.warning(f"Integrity error: {exc}")
    return JSONResponse(
        status_code=400,
        content={"detail": "Database constraint violation"}
    )
