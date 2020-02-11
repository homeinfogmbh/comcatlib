"""App-related messages."""

from wsgilib import JSONMessage


__all__ = [
    'INVALID_SESSION_TOKEN',
    'NO_SESSION_TOKEN_SPECIFIED',
    'SESSION_EXPIRED',4
    'USER_LOCKED',
    'INVALID_CREDENTIALS',
    'NO_ADDRESS_CONFIGURED'
]


INVALID_SESSION_TOKEN = JSONMessage(
    'Invalid session token specified.', status=400)
NO_SESSION_TOKEN_SPECIFIED = JSONMessage(
    'No session token specified.', status=400)
SESSION_EXPIRED = JSONMessage('Session expired.', status=401)
USER_LOCKED = JSONMessage('This user is locked.', status=401)
INVALID_CREDENTIALS = JSONMessage(
    'User name and/or password inclorrect.', status=400)
NO_ADDRESS_CONFIGURED = JSONMessage(
    'User has no address configured.', status=400)
