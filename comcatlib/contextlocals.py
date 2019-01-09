"""Context locals."""

from uuid import UUID

from flask import request
from werkzeug.local import LocalProxy

from comcatlib.orm import Session
from comcatlib.exceptions import NoSessionTokenSpecified
from comcatlib.exceptions import InvalidSessionToken
from comcatlib.exceptions import NoSuchSession


__all__ = ['SESSION']


def get_session():
    """Returns the current session."""

    token = request.cookies.get('session')

    if not token:
        raise NoSessionTokenSpecified()

    try:
        token = UUID(token)
    except ValueError:
        raise InvalidSessionToken()

    try:
        return Session.get(Session.token == token)
    except Session.DoesNotExist:
        raise NoSuchSession()


SESSION = LocalProxy(get_session)
