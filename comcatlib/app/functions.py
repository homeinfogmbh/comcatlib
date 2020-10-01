"""Common functions."""

from uuid import UUID

from flask import request

from wsgilib import JSON

from comcatlib.exceptions import NonceUsed
from comcatlib.messages import INVALID_UUID
from comcatlib.messages import INVALID_NONCE
from comcatlib.messages import MISSING_NONCE
from comcatlib.oauth import SERVER
from comcatlib.oauth.introspection_endpoint import TokenIntrospectionEndpoint
from comcatlib.oauth.revocation_endpoint import TokenRevocationEndpoint
from comcatlib.orm import AuthorizationNonce, Client, InitializationNonce


__all__ = [
    'register_client',
    'authorize_client',
    'revoke_token',
    'introspect_token'
]


def authorize_client():
    """Login is required since we need to know the current resource owner.
    It can be done with a redirection to the login page, or a login
    form on this authorization page.
    """

    nonce = request.json.pop('nonce', None)

    if nonce is None:
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


def introspect_token():
    """Introspects a token."""

    return SERVER.create_endpoint_response(
        TokenIntrospectionEndpoint.ENDPOINT_NAME)


def register_client():
    """Registers a client."""

    nonce = request.json.pop('nonce', None)

    if nonce is None:
        return MISSING_NONCE

    try:
        uuid = UUID(nonce)
    except ValueError:
        return INVALID_UUID

    try:
        user = InitializationNonce.use(uuid)
    except NonceUsed:
        return INVALID_NONCE

    transaction, secret = Client.add(user)
    transaction.commit()
    json = transaction.primary.to_json()
    json['clientSecret'] = secret
    json['authorizationNonce'] = AuthorizationNonce.add(user)
    return JSON(json)


def revoke_token():
    """Revokes a token."""

    return SERVER.create_endpoint_response(
        TokenRevocationEndpoint.ENDPOINT_NAME)
