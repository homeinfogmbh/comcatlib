"""Common functions."""

from secrets import choice
from string import ascii_letters, digits


__all__ = ['genpw']


def genpw(*, pool: str = ascii_letters + digits, length: int = 32) -> str:
    """Generates a random password."""

    return ''.join(choice(pool) for _ in range(length))
