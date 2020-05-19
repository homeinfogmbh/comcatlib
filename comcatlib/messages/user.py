"""User-related messages."""

from wsgilib import JSONMessage


__all__ = [
    'NO_SUCH_CUSTOMER',
    'NO_SUCH_USER',
    'NO_USER_SPECIFIED',
    'USER_ADDED',
    'USER_DELETED',
    'USER_LOCKED',
    'USER_PATCHED'
]


NO_SUCH_CUSTOMER = JSONMessage('No such customer.', status=404)
NO_SUCH_USER = JSONMessage('The requested user does not exists.', status=404)
NO_USER_SPECIFIED = JSONMessage('No user specified.', status=400)
USER_ADDED = JSONMessage('The user has been added.', status=201)
USER_DELETED = JSONMessage('The user has been deleted.', status=200)
USER_LOCKED = JSONMessage('This user is locked.', status=401)
USER_PATCHED = JSONMessage('The user has been modified.', status=200)
