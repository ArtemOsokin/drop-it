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
    DB_UNAVAILABLE = {
        ERROR_CODE: 'service_unavailable',
        ERROR_MESSAGE: 'Сервис недоступен.',
    }


class UserErrorMessage(BaseErrorMessage):
    USER_NOT_FOUND = {
        ERROR_CODE: 'user_not_found',
        ERROR_MESSAGE: 'Пользователь не найден',
    }
    USERNAME_ALREADY_EXIST = {
        ERROR_CODE: 'username_already_exist',
        ERROR_MESSAGE: 'Такой пользователь уже занят',
    }
    EMAIL_ALREADY_EXIST = {
        ERROR_CODE: 'email_already_exist',
        ERROR_MESSAGE: 'Такой email уже занят',
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
    INCORRECT_PASSWORD = {
        ERROR_CODE: 'password_incorrect',
        ERROR_MESSAGE: 'Неправильный пароль',
    }
    INCORRECT_USERNAME = {
        ERROR_CODE: 'username_incorrect',
        ERROR_MESSAGE: 'Неправильно введенный логин',
    }
    PERMISSION_DENIED = {
        ERROR_CODE: 'permission_denied',
        ERROR_MESSAGE: 'Недостаточно прав на данную операцию',
    }


class DropErrorMessage(BaseErrorMessage):
    GENRE_NOT_FOUND = {
        ERROR_CODE: 'genre_not_found',
        ERROR_MESSAGE: 'Жанр отсутствует',
    }
    DROP_NOT_FOUND = {
        ERROR_CODE: 'drop_not_found',
        ERROR_MESSAGE: 'Дроп не найден',
    }
