"""ComCat end user authentication."""

from functools import wraps

from comcatlib.contextlocals import SESSION, get_session_duration
from comcatlib.messages import SESSION_EXPIRED, ACCOUNT_LOCKED


__all__ = ['authenticated']


def authenticated(function):
    """Prepends authentication checks to the respective function."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Wraps the original function."""
        if not SESSION.alive:
            raise SESSION_EXPIRED

        if not SESSION.account.usable:
            raise ACCOUNT_LOCKED

        SESSION.renew(duration=get_session_duration())
        return function(*args, **kwargs)

    return wrapper
