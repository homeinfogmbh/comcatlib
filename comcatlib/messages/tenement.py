"""Tenement-related messages."""

from wsgilib import JSONMessage


__all__ = [
    'INVALID_TENEMENT',
    'NO_SUCH_TENEMENT',
    'TENEMENT_ADDED',
    'TENEMENT_DELETED',
    'TENEMENT_PATCHED'
]


INVALID_TENEMENT = JSONMessage('Invalid value for tenement.', status=400)
NO_SUCH_TENEMENT = JSONMessage(
    'The requested tenement does not eixst.', status=404)
TENEMENT_ADDED = JSONMessage('The tenement has been added.', status=201)
TENEMENT_DELETED = JSONMessage('The tenement has been deleted.', status=200)
TENEMENT_PATCHED = JSONMessage(
    'The requested tenement has been patched.', status=200)
