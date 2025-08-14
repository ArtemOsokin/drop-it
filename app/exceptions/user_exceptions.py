class BaseUserException(Exception):
    pass


class UserNotFound(BaseUserException):
    pass


class UsernameAlreadyExists(BaseUserException):
    pass


class EmailAlreadyExists(BaseUserException):
    pass
