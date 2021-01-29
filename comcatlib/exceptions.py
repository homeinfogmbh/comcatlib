"""Common exceptions."""


__all__ = [
    'DuplicateUser',
    'InvalidAddress',
    'InvalidPassword',
    'NonceUsed',
    'QuotaExceeded',
    'UserExpired',
    'UserLocked'
]


class DuplicateUser(Exception):
    """Indicates a duplicate user."""


class InvalidAddress(Exception):
    """Indicates that an invalid address value was provided."""


class InvalidPassword(Exception):
    """Indicates that the user is locked."""


class NonceUsed(Exception):
    """Indicates that a nonce has already been used."""


class QuotaExceeded(Exception):
    """Indicates that a user has exceeded their disk quota."""


class UserExpired(Exception):
    """Indicates that the user is expired."""


class UserLocked(Exception):
    """Indicates that the user is locked."""
