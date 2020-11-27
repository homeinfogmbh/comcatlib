"""Common exceptions."""


__all__ = [
    'ComCatException',
    'DuplicateUser',
    'NonceUsed',
    'QuotaExceeded',
    'UserExpired',
    'UserLocked'
]


class ComCatException(Exception):
    """Common ComCat exception."""


class DuplicateUser(ComCatException):
    """Indicates a duplicate user."""


class NonceUsed(ComCatException):
    """Indicates that a nonce has already been used."""


class QuotaExceeded(ComCatException):
    """Indicates that a user has exceeded their disk quota."""


class UserExpired(ComCatException):
    """Indicates that the user is expired."""


class UserLocked(ComCatException):
    """Indicates that the user is locked."""


class InvalidPassword(ComCatException):
    """Indicates that the user is locked."""
