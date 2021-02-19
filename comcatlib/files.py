"""User file handling."""

from flask import request

from comcatlib.localproxies import CUSTOMER, USER
from comcatlib.orm.files import UserFile, Quota


__all__ = ['add_file']


def add_file(bytes_: bytes) -> UserFile:
    """Adds a file."""

    quota = Quota.for_customer(CUSTOMER.id)
    quota.alloc(len(bytes_))
    name = request.args.get('filename') or None
    user_file = UserFile.add(USER.id, bytes_, name=name)
    user_file.save()
    return user_file
