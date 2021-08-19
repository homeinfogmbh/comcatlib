"""Common functions."""

from uuid import UUID

from flask import request, Response

from wsgilib import JSON

from comcatlib.exceptions import InvalidPassword
from comcatlib.exceptions import NonceUsed
from comcatlib.exceptions import UserExpired
from comcatlib.exceptions import UserLocked
from comcatlib.messages import INVALID_CREDENTIALS
from comcatlib.messages import INVALID_UUID
from comcatlib.messages import INVALID_NONCE
from comcatlib.messages import MISSING_NONCE
from comcatlib.messages import MISSING_USER_ID
from comcatlib.messages import MISSING_USER_PW
from comcatlib.messages import USER_EXPIRED
from comcatlib.messages import USER_LOCKED
from comcatlib.oauth import SERVER
from comcatlib.oauth.introspection_endpoint import TokenIntrospectionEndpoint
from comcatlib.oauth.revocation_endpoint import TokenRevocationEndpoint
from comcatlib.orm import AuthorizationNonce, Client, User


__all__ = [
    'register_client',
    'authorize_client',
    'revoke_token',
    'introspect_token'
]


def authorize_client() -> Response:
    """Login is required since we need to know the current resource owner.
    It can be done with a redirection to the login page, or a login
    form on this authorization page.
    """

    if (nonce := request.form.get('nonce')) is None:
        return MISSING_NONCE

    try:
        uuid = UUID(nonce)
    except ValueError:
        return INVALID_UUID

    try:
        user = AuthorizationNonce.use(uuid)
    except NonceUsed:
        return INVALID_NONCE

    return SERVER.create_authorization_response(grant_user=user)


def introspect_token() -> Response:
    """Introspects a token."""

    return SERVER.create_endpoint_response(
        TokenIntrospectionEndpoint.ENDPOINT_NAME)


def register_client() -> JSON:
    """Registers a client."""

    if (ident := request.json.get('id')) is None:
        return MISSING_USER_ID

    if (passwd := request.json.get('passwd')) is None:
        return MISSING_USER_PW

    try:
        user = User[ident]
    except User.DoesNotExist:
        return INVALID_CREDENTIALS

    try:
        user.login(passwd)
    except UserLocked:
        return USER_LOCKED
    except UserExpired:
        return USER_EXPIRED
    except InvalidPassword:
        return INVALID_CREDENTIALS

    transaction, secret = Client.add(user)
    transaction.commit()
    json = transaction.primary.to_json()
    json['clientSecret'] = secret
    json['authorizationNonce'] = AuthorizationNonce.add(user).uuid.hex
    return JSON(json)


def revoke_token() -> Response:
    """Revokes a token."""

    return SERVER.create_endpoint_response(
        TokenRevocationEndpoint.ENDPOINT_NAME)
