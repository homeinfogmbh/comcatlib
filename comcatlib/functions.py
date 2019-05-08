"""Common functions."""

from comcatlib.contextlocals import CUSTOMER
from comcatlib.messages import NO_SUCH_ACCOUNT
from comcatlib.orm import Account


__all__ = ['get_account']


def get_account(ident):
    """Returns the respective account."""

    try:
        return Account.get(
            (Account.id == ident) & (Account.customer == CUSTOMER.id))
    except Account.DoesNotExist:
        raise NO_SUCH_ACCOUNT
