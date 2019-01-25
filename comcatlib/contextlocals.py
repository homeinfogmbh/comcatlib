"""Context locals."""

from uuid import UUID

from flask import request
from werkzeug.local import LocalProxy

from mdb import Customer

from comcatlib.config import ALLOWED_SESSION_DURATIONS
from comcatlib.config import DEFAULT_SESSION_DURATION
from comcatlib.exceptions import InvalidSessionToken
from comcatlib.exceptions import NoSessionTokenSpecified
from comcatlib.exceptions import NoSuchSession
from comcatlib.messages import NO_SUCH_ACCOUNT
from comcatlib.messages import NO_SUCH_CUSTOMER
from comcatlib.orm import Account, Session


__all__ = ['ACCOUNT', 'CUSTOMER', 'SESSION', 'get_session_duration']


def _account_by_string(string):
    """Returns an account by its UUID string."""

    try:
        uuid = UUID(string)
    except ValueError:
        raise NO_SUCH_ACCOUNT

    try:
        return Account.get(Account.uuid == uuid)
    except Account.DoesNotExist:
        raise NO_SUCH_ACCOUNT


def _customer_by_string(string):
    """Returns a customer by its CID."""

    try:
        cid = int(string)
    except ValueError:
        raise NO_SUCH_CUSTOMER

    try:
        return Customer.get(Customer.id == cid)
    except Customer.DoesNotExist:
        raise NO_SUCH_CUSTOMER


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


def get_customer():
    """Returns the respective customer."""

    if SESSION.account.root:
        customer = request.headers.get('ComCat-Substitute-Customer')

        if customer:
            return _customer_by_string(customer)

    return ACCOUNT.customer


def get_session_duration():
    """Returns the respective session duration."""

    try:
        duration = int(request.headers['session-duration'])
    except (KeyError, TypeError, ValueError):
        return DEFAULT_SESSION_DURATION

    if duration in ALLOWED_SESSION_DURATIONS:
        return duration

    return DEFAULT_SESSION_DURATION


SESSION = LocalProxy(get_session)
ACCOUNT = LocalProxy(get_account)
CUSTOMER = LocalProxy(get_customer)
