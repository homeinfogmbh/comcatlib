"""User-related messages."""

from wsgilib import JSONMessage


__all__ = [
    "DUPLICATE_USER",
    "MISSING_USER_PW",
    "NO_SUCH_USER",
    "USER_ADDED",
    "USER_DELETED",
    "USER_PATCHED",
]


DUPLICATE_USER = JSONMessage("Duplicate user.", status=400)
MISSING_USER_PW = JSONMessage("Missing user password.", status=400)
NO_SUCH_USER = JSONMessage("The requested user does not exists.", status=404)
USER_ADDED = JSONMessage("The user has been added.", status=201)
USER_DELETED = JSONMessage("The user has been deleted.", status=200)
USER_PATCHED = JSONMessage("The user has been modified.", status=200)
