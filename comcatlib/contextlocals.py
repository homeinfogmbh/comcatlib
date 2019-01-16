"""Context locals."""

from uuid import UUID

from flask import request
from werkzeug.local import LocalProxy

from comcatlib.orm import Account, Session
from comcatlib.exceptions import NoSessionTokenSpecified
from comcatlib.exceptions import InvalidSessionToken
from comcatlib.exceptions import NoSuchSession
from comcatlib.messages import NoSuchAccount


__all__ = ['ACCOUNT', 'CUSTOMER', 'SESSION']


def _account_by_string(string):
    """Returns an account by its UUID string."""

    try:
        uuid = UUID(string)
    except ValueError:
        raise NoSuchAccount()

    try:
        return Account.get(Account.uuid == uuid)
    except Account.DoesNotExist:
        raise NoSuchAccount()


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


def get_account():
    """Returns the respective account."""

    account = SESSION.account

    if account.root:
        su_account = request.headers.get('ComCat-Substitute-Account')

        if su_account:
            return _account_by_string(su_account)

    return account


SESSION = LocalProxy(get_session)
ACCOUNT = LocalProxy(get_account)
CUSTOMER = LocalProxy(lambda: ACCOUNT.customer)
