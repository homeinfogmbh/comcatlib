"""Common exceptions."""


__all__ = [
    'AlreadyRegistered',
    'DuplicateUser',
    'InvalidAddress',
    'InvalidPassword',
    'NonceUsed',
    'PasswordResetPending',
    'QuotaExceeded',
    'UserExpired',
    'UserLocked'
]


class AlreadyRegistered(Exception):
    """Indicates that the respective tenant ID is alerady registered."""

    def __init__(self, record):
        super().__init__(record)
        self.record = record


class DuplicateUser(Exception):
    """Indicates a duplicate user."""


class InvalidAddress(Exception):
    """Indicates that an invalid address value was provided."""


class InvalidPassword(Exception):
    """Indicates that the user is locked."""


class NonceUsed(Exception):
    """Indicates that a nonce has already been used."""


class PasswordResetPending(Exception):
    """Indicates that a password reset is already pending."""


class QuotaExceeded(Exception):
    """Indicates that a user has exceeded their disk quota."""

    def __init__(self, quota: int, free: int, size: int):
        super().__init__()
        self.quota = quota
        self.free = free
        self.size = size


class UserExpired(Exception):
    """Indicates that the user is expired."""


class UserLocked(Exception):
    """Indicates that the user is locked."""
