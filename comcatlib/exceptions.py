"""Common exceptions."""


__all__ = [
    'ComCatException',
    'UserLocked',
    'DurationOutOfBounds',
    'InvalidSession',
    'InvalidSessionToken',
    'InvalidCredentials',
    'NoSessionTokenSpecified',
    'NoSuchSession',
    'NoSuchBaseChart'
]


class ComCatException(Exception):
    """Common ComCat exception."""


class UserLocked(ComCatException):
    """Indicates that the respective user is locked."""


class DurationOutOfBounds(ComCatException):
    """Indicates that the requested session duration is out of bounds."""


class InvalidSession(ComCatException):
    """Indicates an invalid session."""


class InvalidSessionToken(ComCatException):
    """Indicates that an invalid session token was specified."""


class InvalidCredentials(ComCatException):
    """Indicates that an invalid account name or password were provided."""


class NoSessionTokenSpecified(ComCatException):
    """Indicates that no session token was specified."""


class NoSuchSession(ComCatException):
    """Indicates that a respective session does not exist."""


class NoSuchBaseChart(ComCatException):
    """Indicates that the respective base chart was not found."""
