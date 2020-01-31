"""OAuth 2.0 authorization server."""

from authlib.integrations.flask_oauth2 import AuthorizationServer

from comcatlib.orm.oauth import Client, Token


__all__ = ['SERVER']


def query_client(client_id):
    """Returns a c lient by its ID."""

    return Client.get(client_id=client_id)


def save_token(token_data, request):
    """Stores the respective token."""

    if request.user:
        user_id = request.user.get_user_id()
    else:
        # client_credentials grant_type
        user_id = request.client.user_id
        # or, depending on how you treat client_credentials
        user_id = None

    client_id = request.client.client_id
    token = Token(client_id=client_id, user_id=user_id, **token_data)
    token.save()


SERVER = AuthorizationServer(query_client=query_client, save_token=save_token)
