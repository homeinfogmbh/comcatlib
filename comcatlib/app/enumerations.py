"""Common enumerations."""

from enum import Enum


__all__ = ['GrantType']


class GrantType(Enum):
    """OAuth 2.0 grant types."""

    AUTHORIZATION_CODE = 'authorization_code'
