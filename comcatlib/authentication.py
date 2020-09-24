"""Authentication checks."""

from authlib.integrations.flask_oauth2 import current_token
from werkzeug.local import LocalProxy

from comcatlib.exceptions import UserExpired, UserLocked


__all__ = ['ADDRESS', 'CUSTOMER', 'TENEMENT', 'USER', 'get_user']


def get_user():
    """Performs authentication checks."""

    user = current_token.user

    if user.expired:
        raise UserExpired()

    if user.locked:
        raise UserLocked()

    return user


USER = LocalProxy(get_user)
TENEMENT = LocalProxy(lambda: USER.tenement)
ADDRESS = LocalProxy(lambda: TENEMENT.address)
CUSTOMER = LocalProxy(lambda: TENEMENT.customer)