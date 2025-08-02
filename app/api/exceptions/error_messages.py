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
    USER_UNAUTHORIZED = {
        ERROR_CODE: 'user_unauthorized',
        ERROR_MESSAGE: 'Пользователь не авторизован.',
    }


class UserErrorMessage(BaseErrorMessage):
    USER_NOT_FOUND = {
        ERROR_CODE: 'user_not_found',
        ERROR_MESSAGE: 'Пользователь не найден',
    }


class AuthErrorMessage(BaseErrorMessage):
    USER_ALREADY_EXIST_EMAIL = {
        ERROR_CODE: 'user_already_exist_email',
        ERROR_MESSAGE: 'Пользователь с таким Email уже существует',
    }

    USER_ALREADY_EXIST_USERNAME = {
        ERROR_CODE: 'user_already_exist_username',
        ERROR_MESSAGE: 'Пользователь с таким Логином уже существует',
    }
