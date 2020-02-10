"""Common functions."""

from his import CUSTOMER

from comcatlib.messages import NO_SUCH_USER
from comcatlib.orm.user import User


__all__ = ['get_user']


def get_user(ident):
    """Returns the respective user."""

    try:
        return User.get((User.id == ident) & (User.customer == CUSTOMER.id))
    except User.DoesNotExist:
        raise NO_SUCH_USER
