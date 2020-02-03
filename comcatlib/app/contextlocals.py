"""Context locals."""

from uuid import UUID

from flask import request
from werkzeug.local import LocalProxy

from mdb import Customer

from comcatlib.exceptions import InvalidSessionToken
from comcatlib.exceptions import NoSessionTokenSpecified
from comcatlib.exceptions import NoSuchSession
from comcatlib.messages import NO_SUCH_USER
from comcatlib.messages import NO_SUCH_CUSTOMER
from comcatlib.orm import Session, User


__all__ = ['USER', 'CUSTOMER', 'SESSION']


def _user_by_string(string):
    """Returns a user account by its UUID string."""

    try:
        uuid = UUID(string)
    except ValueError:
        raise NO_SUCH_USER

    try:
        return User.get(User.uuid == uuid)
    except User.DoesNotExist:
        raise NO_SUCH_USER


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


def get_user():
    """Returns the respective user account."""

    user = SESSION.user

    if user.root:
        su_user = request.headers.get('ComCat-Substitute-User')

        if su_user:
            return _user_by_string(su_user)

    return user


def get_customer():
    """Returns the respective customer."""

    if SESSION.user.root:
        customer = request.headers.get('ComCat-Substitute-Customer')

        if customer:
            return _customer_by_string(customer)

    return USER.customer


SESSION = LocalProxy(get_session)
USER = LocalProxy(get_user)
CUSTOMER = LocalProxy(get_customer)
