"""OAuth 2.0 authorization server."""

from authlib.integrations.flask_oauth2 import AuthorizationServer
from authlib.oauth2.rfc6749.grants import ImplicitGrant

from comcatlib.oauth.authorization_code_grant import AuthorizationCodeGrant
from comcatlib.oauth.introspection_endpoint import TokenIntrospectionEndpoint
from comcatlib.oauth.refresh_token_grant import RefreshTokenGrant
from comcatlib.oauth.revocation_endpoint import TokenRevocationEndpoint
from comcatlib.openid import OpenIDCode
from comcatlib.orm.oauth import Client, Token


__all__ = ['SERVER', 'init_oauth']


def query_client(client_id):
    """Returns a c lient by its ID."""

    try:
        return Client.get(Client.client_id == client_id)
    except Client.DoesNotExist:
        return None


def save_token(token_data, request):
    """Stores the respective token."""

    if request.user:
        print('User set.', flush=True)
        user_id = request.user.id
    else:
        print('User NOT set.', flush=True)
        user_id = request.client.user_id

    print('User ID:', user_id, flush=True)
    client_id = request.client.client_id
    print('Client ID:', client_id, flush=True)
    token = Token(client_id=client_id, user_id=user_id, **token_data)
    token.save()


SERVER = AuthorizationServer(query_client=query_client, save_token=save_token)


def init_oauth(application):
    """Initializes OAuth 2.0 for the given application."""

    openid = OpenIDCode(require_nonce=True)
    SERVER.init_app(application)
    SERVER.register_grant(AuthorizationCodeGrant, [openid])
    SERVER.register_grant(RefreshTokenGrant)
    SERVER.register_grant(ImplicitGrant)
    SERVER.register_endpoint(TokenRevocationEndpoint)
    SERVER.register_endpoint(TokenIntrospectionEndpoint)
