"""Common functions."""

from flask import request

from comcatlib.config import ALLOWED_SESSION_DURATIONS
from comcatlib.config import DEFAULT_SESSION_DURATION


__all__ = ['get_account', 'get_session_duration']


def get_account(ident):
    """Returns the respective account."""

    return Account.get(
        (Account.id == ident) & (Account.customer == CUSTOMER.id))


def get_session_duration():
    """Returns the respective session duration."""

    try:
        duration = int(request.headers['session-duration'])
    except (KeyError, TypeError, ValueError):
        return DEFAULT_SESSION_DURATION

    if duration in ALLOWED_SESSION_DURATIONS:
        return duration

    return DEFAULT_SESSION_DURATION
