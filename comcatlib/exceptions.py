"""Common exceptions."""


__all__ = [
    'ComCatException',
    'DuplicateUser',
    'DurationOutOfBounds',
    'InvalidSession',
    'InvalidSessionToken',
    'InvalidCredentials',
    'NonceUsed',
    'NoSuchBaseChart',
    'QuotaExceeded',
    'UserExpired',
    'UserLocked'
]


class ComCatException(Exception):
    """Common ComCat exception."""


class DuplicateUser(ComCatException):
    """Indicates a duplicate user."""


class DurationOutOfBounds(ComCatException):
    """Indicates that the requested session duration is out of bounds."""


class InvalidSession(ComCatException):
    """Indicates an invalid session."""


class InvalidSessionToken(ComCatException):
    """Indicates that an invalid session token was specified."""


class InvalidCredentials(ComCatException):
    """Indicates that an invalid account name or password were provided."""


class NonceUsed(ComCatException):
    """Indicates that a nonce has already been used."""


class NoSuchBaseChart(ComCatException):
    """Indicates that the respective base chart was not found."""


class QuotaExceeded(ComCatException):
    """Indicates that a user has exceeded their disk quota."""


class UserExpired(ComCatException):
    """Indicates that the user is expired."""


class UserLocked(ComCatException):
    """Indicates that the user is locked."""
