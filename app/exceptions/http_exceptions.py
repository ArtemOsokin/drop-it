from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette import status

from app.exceptions.error_messages import BaseErrorMessage, HTTPErrorMessage


class BaseApiException(Exception):  # pragma: no cover
    status_code: int

    def __init__(
        self,
        *,
        enum_error: BaseErrorMessage | None = None,
        error_code: str | None = None,
        error_message: str | None = None,
        **format_params,
    ):
        has_enum_in_kwargs = bool(enum_error)
        has_text_errors_in_kwargs = bool(error_code and error_message)
        assert (
            has_enum_in_kwargs ^ has_text_errors_in_kwargs
        ), 'Allowed error_code and error_message XOR enum_error'

        if has_enum_in_kwargs:
            error_code = enum_error.error_code
            error_message = enum_error.error_message.format(**format_params)

        self.error_code = error_code
        self.error_message = error_message

    def get_response_data(self):
        return JSONResponse(
            content={
                'error': {
                    'error_code': self.error_code,
                    'error_message': self.error_message,
                },
            },
            status_code=self.status_code,
        )


class BadRequest(BaseApiException):  # pragma: no cover
    status_code = status.HTTP_400_BAD_REQUEST


class Unauthorized(BaseApiException):  # pragma: no cover
    status_code = status.HTTP_401_UNAUTHORIZED


class NotFound(BaseApiException):  # pragma: no cover
    status_code = status.HTTP_404_NOT_FOUND


class NotAcceptable(BaseApiException):  # pragma: no cover
    status_code = status.HTTP_406_NOT_ACCEPTABLE


class InternalServerError(BaseApiException):  # pragma: no cover
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class ServiceUnavailableError(BaseApiException):  # pragma: no cover
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE


class AccessForbidden(BaseApiException):
    status_code = status.HTTP_403_FORBIDDEN
