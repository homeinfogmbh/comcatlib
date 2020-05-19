"""Login-related messages."""

from wsgilib import JSONMessage


__all__ = ['INVALID_CREDENTIALS', 'MISSING_PASSWORD']


INVALID_CREDENTIALS = JSONMessage('Invalid credentials.', status=400)
MISSING_PASSWORD = JSONMessage('No password specified.', status=400)
