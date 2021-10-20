"""Token introspection endpoint."""

from typing import Optional

from authlib.oauth2.rfc7662 import IntrospectionEndpoint

from comcatlib.orm.oauth import Client, Token


__all__ = ['TokenIntrospectionEndpoint']


URL = 'https://comcat.homeinfo.de/'


def get_token(token: str, token_type_hint: str) -> Token:
    """Returns the respective token."""

    if token_type_hint == 'access_token':
        condition = Token.access_token == token
    elif token_type_hint == 'refresh_token':
        condition = Token.refresh_token == token
    else:
        condition = Token.access_token == token
        condition |= Token.refresh_token == token

    return Token.select(cascade=True).where(condition).get()


# pylint: disable=R0201
class TokenIntrospectionEndpoint(IntrospectionEndpoint):
    """Introspection of bearer tokens."""

    TOKEN_ENDPOINT_AUTH_METHODS = ['client_secret_post']

    def query_token(self, token: Token, token_type_hint: str,
                    client: Client) -> Optional[Token]:
        """Returns the respective token."""
        try:
            token = get_token(token, token_type_hint)
        except Token.DoesNotExist:
            return None

        if token.client_id == client.client_id:
            return token

        return None

    def introspect_token(self, token: Token) -> dict:
        """Returns a JSON-ish dict of the token."""
        return {
            'active': True,
            'client_id': token.client_id,
            'token_type': token.token_type,
            'username': token.user.uuid.hex,
            'scope': token.get_scope(),
            'sub': token.user.uuid.hex,
            'aud': token.client_id,
            'iss': URL,
            'exp': token.expires_at,
            'iat': token.issued_at,
        }
