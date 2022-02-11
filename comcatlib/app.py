"""Backend for the smartphone apps."""

from uuid import UUID

from flask import request, Flask, Response

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
from comcatlib.oauth2 import FRAMEWORK
from comcatlib.orm import AuthorizationNonce, User
from comcatlib.pwgen import genpw


__all__ = ['init_oauth_endpoints']


def init_oauth_endpoints(application: Flask) -> None:
    """Adds OAuth endpoints to the respective application."""

    application.route('/client', methods=['POST'])(register_client)
    application.route('/authorize', methods=['POST'])(authorize_client)
    application.route('/oauth/token', methods=['POST'])(
        FRAMEWORK.authorization_server.create_token_response
    )
    application.route('/oauth/revoke', methods=['POST'])(
        FRAMEWORK.authorization_server.revoke_token
    )
    application.route('/oauth/introspect', methods=['POST'])(
        FRAMEWORK.authorization_server.introspect_token
    )


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
        user = AuthorizationNonce.use(uuid).user
    except NonceUsed:
        return INVALID_NONCE

    return FRAMEWORK.authorization_server.create_authorization_response(
        grant_user=user
    )


def register_client() -> JSON:  # pylint: disable=R0911
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

    transaction = FRAMEWORK.models.client.add(user, secret := genpw())
    transaction.commit()
    json = transaction.primary.to_json()
    json['clientSecret'] = secret
    json['authorizationNonce'] = AuthorizationNonce.add(user).uuid.hex
    return JSON(json)
