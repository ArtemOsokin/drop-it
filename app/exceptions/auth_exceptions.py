class BaseAuthException(Exception):
    pass


class UserAlreadyExistsEmail(BaseAuthException):
    pass


class UserAlreadyExistsUsername(BaseAuthException):
    pass


class IncorrectPassword(BaseAuthException):
    pass


class IncorrectUsername(BaseAuthException):
    pass

class PermissionDenied(BaseAuthException):
    pass
