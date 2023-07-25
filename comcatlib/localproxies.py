"""Local proxies for authentication checks."""

from authlib.integrations.flask_oauth2 import current_token
from werkzeug.local import LocalProxy

from comcatlib.exceptions import UserExpired, UserLocked
from comcatlib.orm.user import User


__all__ = ["ADDRESS", "CUSTOMER", "TENEMENT", "USER", "get_user"]


def get_user() -> User:
    """Performs authentication checks."""

    if (
        user := User.select(cascade=True).where(User.id == current_token.user).get()
    ).expired:
        raise UserExpired()

    if user.locked:
        raise UserLocked()

    return user


USER = LocalProxy(get_user)
TENEMENT = LocalProxy(lambda: USER.tenement)
ADDRESS = LocalProxy(lambda: TENEMENT.address)
CUSTOMER = LocalProxy(lambda: TENEMENT.customer)
