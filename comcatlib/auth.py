"""ComCat end user authentication."""

from functools import wraps

from flask import request

from comcatlib.config import ALLOWED_SESSION_DURATIONS
from comcatlib.config import DEFAULT_SESSION_DURATION
from comcatlib.contextlocals import SESSION
from comcatlib.messages import SESSION_EXPIRED, ACCOUNT_LOCKED


__all__ = ['get_session_duration', 'authenticated']


def get_session_duration():
    """Returns the respective session duration."""

    try:
        duration = int(request.headers['session-duration'])
    except (KeyError, TypeError, ValueError):
        return DEFAULT_SESSION_DURATION

    if duration in ALLOWED_SESSION_DURATIONS:
        return duration

    return DEFAULT_SESSION_DURATION


def authenticated(function):
    """Prepends authentication checks to the respective function."""

    @wraps(function)
    def wrapper(*args, **kwargs):
        """Wraps the original function."""
        if not SESSION.alive:
            raise SESSION_EXPIRED

        if not SESSION.account.can_login:
            raise ACCOUNT_LOCKED

        SESSION.renew(duration=get_session_duration())
        return function(*args, **kwargs)

    return wrapper
