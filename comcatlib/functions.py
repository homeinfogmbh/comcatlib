"""Common functions."""

from flask import request

from cmslib.messages.group import NO_SUCH_GROUP
from cmslib.orm.group import Group

from comcatlib.config import ALLOWED_SESSION_DURATIONS
from comcatlib.config import DEFAULT_SESSION_DURATION
from comcatlib.contextlocals import CUSTOMER
from comcatlib.messages import NO_SUCH_ACCOUNT
from comcatlib.orm import Account


__all__ = ['get_account', 'get_group', 'get_session_duration']


def get_account(ident):
    """Returns the respective account."""

    try:
        return Account.get(
            (Account.id == ident) & (Account.customer == CUSTOMER.id))
    except Account.DoesNotExist:
        raise NO_SUCH_ACCOUNT


def get_group(gid):
    """Returns a group for the current user."""

    try:
        return Group.get((Group.id == gid) & (Group.customer == CUSTOMER.id))
    except Group.DoesNotExist:
        raise NO_SUCH_GROUP


def get_session_duration():
    """Returns the respective session duration."""

    try:
        duration = int(request.headers['session-duration'])
    except (KeyError, TypeError, ValueError):
        return DEFAULT_SESSION_DURATION

    if duration in ALLOWED_SESSION_DURATIONS:
        return duration

    return DEFAULT_SESSION_DURATION
