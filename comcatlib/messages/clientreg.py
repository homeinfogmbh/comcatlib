"""Client registration messages."""

from wsgilib import JSONMessage


__all__ = ['INVALID_UUID', 'INVALID_NONCE', 'MISSING_NONCE']


INVALID_UUID = JSONMessage('Invalid UUID.', status=400)
INVALID_NONCE = JSONMessage('Invalid nonde.', status=400)
MISSING_NONCE = JSONMessage('Missing nonce.', status=400)
