from enum import Enum

ERROR_CODE = 'error_code'
ERROR_MESSAGE = 'error_message'


class BaseErrorMessage(dict, Enum):  # pragma: no cover
    @property
    def error_code(self) -> str:
        return self.value[ERROR_CODE]

    @property
    def error_message(self) -> str:
        return self.value[ERROR_MESSAGE]


class HTTPErrorMessage(BaseErrorMessage):
    # pragma: no cover
    INCORRECT_DATA = {
        ERROR_CODE: 'incorrect_data',
        ERROR_MESSAGE: 'Некорректные данные: {verbose_errors}.',
    }


class UserErrorMessage(BaseErrorMessage):
    USER_NOT_FOUND = {
        ERROR_CODE: 'user_not_found',
        ERROR_MESSAGE: 'Пользователь не найден',
    }
