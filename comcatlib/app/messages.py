"""App-related messages."""

from wsgilib import JSONMessage


__all__ = [
    'SESSION_EXPIRED',
    'USER_LOCKED',
    'INVALID_CREDENTIALS',
    'NO_ADDRESS_CONFIGURED'
]


SESSION_EXPIRED = JSONMessage('Session expired.', status=401)
USER_LOCKED = JSONMessage('This user is locked.', status=401)
INVALID_CREDENTIALS = JSONMessage(
    'User name and/or password inclorrect.', status=400)
NO_ADDRESS_CONFIGURED = JSONMessage(
    'User has no address configured.', status=400)
