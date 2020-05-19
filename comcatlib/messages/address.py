"""Address-related messages."""

from wsgilib import JSONMessage


__all__ = [
    'ADDRESS_ADDED',
    'ADDRESS_DELETED',
    'INVALID_ADDRESS',
    'MISSING_ADDRESS',
    'NO_SUCH_ADDRESS'
]

ADDRESS_ADDED = JSONMessage('The address has been added.', status=201)
ADDRESS_DELETED = JSONMessage('The address has been deleted.', status=200)
INVALID_ADDRESS = JSONMessage('Invalid value for address.', status=400)
MISSING_ADDRESS = JSONMessage('Account has no address configured.', status=400)
NO_SUCH_ADDRESS = JSONMessage('No such address.', status=404)
