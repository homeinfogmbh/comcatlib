"""Toaken revication endpoint."""

from typing import Optional

from authlib.oauth2.rfc7009 import RevocationEndpoint

from comcatlib.orm.oauth import Client, Token


__all__ = ['TokenRevocationEndpoint']


# pylint: disable=R0201
class TokenRevocationEndpoint(RevocationEndpoint):
    """A Token revocation endpoint."""

    CLIENT_AUTH_METHODS = ['client_secret_post']

    def query_token(self, token: str, token_type_hint: str,
                    client: Client) -> Optional[Token]:
        """Queries a token from the database."""
        condition = Token.client_id == client.client_id
        access_token = Token.access_token == token
        refresh_token = Token.refresh_token == token

        if token_type_hint == 'access_token':
            condition &= access_token
        elif token_type_hint == 'refresh_token':
            condition &= refresh_token
        else:   # without token_type_hint
            condition &= access_token | refresh_token

        try:
            return Token.get(condition)
        except Token.DoesNotExist:
            return None

    def revoke_token(self, token: Token) -> None:
        """Revokes the respective token."""
        token.revoked = True
        token.save()
