"""OAuth 2.0 authorization server."""

from typing import Any, Optional

from flask import Flask

from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.oauth2.rfc6749.grants import ImplicitGrant

from comcatlib.oauth.authorization_code_grant import AuthorizationCodeGrant
from comcatlib.oauth.introspection_endpoint import TokenIntrospectionEndpoint
from comcatlib.oauth.refresh_token_grant import RefreshTokenGrant
from comcatlib.oauth.revocation_endpoint import TokenRevocationEndpoint
from comcatlib.orm.oauth import Client, Token


__all__ = ['SERVER', 'init_oauth']


def query_client(client_id: int) -> Optional[Client]:
    """Returns a c lient by its ID."""

    try:
        return Client.select(cascade=True).where(
            Client.client_id == client_id).get()
    except Client.DoesNotExist:
        return None


def save_token(token_data: dict, request: Any) -> None:
    """Stores the respective token."""

    if request.user:
        user_id = request.user.id
    else:
        user_id = request.client.user_id

    client_id = request.client.client_id
    token = Token(client_id=client_id, user_id=user_id, **token_data)
    token.save()


class AuthorizationServer(AuthorizationServer):
    """Subclass of the original flask authorization server."""

    def create_authorization_response(self, *args, **kwargs) -> Any:
        """Enhanced authorization response generation."""
        result = super().create_authorization_response(*args, **kwargs)
        print('AUTHORIZATION RESPONSE:', type(result), result, flush=True)
        return result


SERVER = AuthorizationServer(query_client=query_client, save_token=save_token)


def init_oauth(application: Flask):
    """Initializes OAuth 2.0 for the given application."""

    SERVER.init_app(application)
    SERVER.register_grant(AuthorizationCodeGrant)
    SERVER.register_grant(RefreshTokenGrant)
    SERVER.register_grant(ImplicitGrant)
    SERVER.register_endpoint(TokenRevocationEndpoint)
    SERVER.register_endpoint(TokenIntrospectionEndpoint)
