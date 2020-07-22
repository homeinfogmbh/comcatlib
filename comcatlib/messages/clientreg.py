"""Client registration messages."""

from wsgilib import JSONMessage


__all__ = ['INVALID_TOKEN', 'NO_TOKEN_SPECIFIED']

INVALID_TOKEN = JSONMessage('Invalid token.', status=400)
NO_TOKEN_SPECIFIED = JSONMessage('No token specified.', status=400)
