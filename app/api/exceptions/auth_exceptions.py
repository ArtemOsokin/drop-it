from app.api.exceptions.user_exceptions import BaseUserException


class BaseAuthException(Exception):
    pass


class UserAlreadyExistsEmail(BaseUserException):
    pass


class UserAlreadyExistsUsername(BaseUserException):
    pass


class IncorrectPassword(BaseUserException):
    pass


class IncorrectUsername(BaseUserException):
    pass
