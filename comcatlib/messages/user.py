"""User-related messages."""

from wsgilib import JSONMessage


__all__ = [
    'DUPLICATE_USER',
    'INVALID_CREDENTIALS',
    'MISSING_USER_ID',
    'MISSING_USER_PW',
    'NO_SUCH_USER',
    'USER_ADDED',
    'USER_DELETED',
    'USER_EXPIRED',
    'USER_LOCKED',
    'USER_PATCHED'
]


DUPLICATE_USER = JSONMessage('Duplicate user.', status=400)
INVALID_CREDENTIALS = JSONMessage('Invalid credentials.', status=400)
MISSING_USER_ID = JSONMessage('Missing user ID.', status=400)
MISSING_USER_PW = JSONMessage('Missing user password.', status=400)
NO_SUCH_USER = JSONMessage('The requested user does not exists.', status=404)
USER_ADDED = JSONMessage('The user has been added.', status=201)
USER_DELETED = JSONMessage('The user has been deleted.', status=200)
USER_EXPIRED = JSONMessage('This user is expired.', status=401)
USER_LOCKED = JSONMessage('This user is locked.', status=401)
USER_PATCHED = JSONMessage('The user has been modified.', status=200)
