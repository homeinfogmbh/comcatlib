"""OAuth 2.0 authorization server."""

from authlib.integrations.flask_oauth2 import AuthorizationServer

from comcatlib.oauth.authorization_code_grant import AuthorizationCodeGrant
from comcatlib.oauth.introspection_endpoint import TokenIntrospectionEndpoint
from comcatlib.oauth.refresh_token_grant import RefreshTokenGrant
from comcatlib.oauth.revocation_endpoint import TokenRevocationEndpoint
from comcatlib.orm.oauth import Client, Token


__all__ = ['SERVER', 'init_oauth']


def query_client(client_id):
    """Returns a c lient by its ID."""

    return Client.get(Client.client_id=client_id)


def save_token(token_data, request):
    """Stores the respective token."""

    if request.user:
        user_id = request.user.get_user_id()
    else:
        user_id = request.client.user_id

    client_id = request.client.client_id
    token = Token(client_id=client_id, user_id=user_id, **token_data)
    token.save()


SERVER = AuthorizationServer(query_client=query_client, save_token=save_token)


def init_oauth(application):
    """Initializes OAuth 2.0 for the given application."""

    SERVER.init_app(application)
    SERVER.register_grant(AuthorizationCodeGrant)
    SERVER.register_grant(RefreshTokenGrant)
    SERVER.register_endpoint(TokenRevocationEndpoint)
    SERVER.register_endpoint(TokenIntrospectionEndpoint)
