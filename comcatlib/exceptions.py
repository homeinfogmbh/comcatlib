"""Common exceptions."""


__all__ = [
    'ComCatException',
    'AccountLocked',
    'DurationOutOfBounds',
    'InvalidSession',
    'InvalidSessionToken',
    'InvalidCredentials',
    'NoSessionTokenSpecified',
    'NoSuchSession']


class ComCatException(Exception):
    """Common ComCat exception."""


class AccountLocked(ComCatException):
    """Indicates that the respective account is locked."""


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
