"""User file handling."""

from flask import request

from comcatlib.authentication import CUSTOMER, USER
from comcatlib.exceptions import QuotaExceeded
from comcatlib.orm.files import UserFile, Quota
from comcatlib.messages.files import QUOTA_EXCEEDED


__all__ = ['add_file']


def add_file(bytes_):
    """Adds a file."""

    quota = Quota.for_customer(CUSTOMER.id)

    try:
        quota.alloc(len(bytes_))
    except QuotaExceeded:
        raise QUOTA_EXCEEDED from None

    name = request.args.get('filename') or None
    user_file = UserFile.add(USER.id, bytes_, name=name)
    user_file.save()
    return user_file
