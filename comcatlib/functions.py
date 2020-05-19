"""Common functions."""

from authlib.integrations.flask_oauth2 import current_token
from his import CUSTOMER

from comcatlib.messages import NO_SUCH_USER, QUOTA_EXCEEDED
from comcatlib.orm.user import File, Quota, User


__all__ = ['get_user']


def get_user(ident):
    """Returns the respective user."""

    try:
        return User.get((User.id == ident) & (User.customer == CUSTOMER.id))
    except User.DoesNotExist:
        raise NO_SUCH_USER


def add_file(bytes_):
    """Adds a file."""

    quota = Quota.for_customer(current_token.user.customer_id)

    try:
        quota.alloc(len(bytes_))
    except QuotaExceeded:
        raise QUOTA_EXCEEDED

    file = File.add(bytes_)
    file.save()
    return file
