class BaseDropException(Exception):
    pass


class GenreNotFound(BaseDropException):
    pass


class DropNotFound(BaseDropException):
    pass
