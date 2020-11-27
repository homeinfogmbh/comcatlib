"""Toaken revication endpoint."""

from authlib.oauth2.rfc7009 import RevocationEndpoint

from comcatlib.orm.oauth import Client, Token


__all__ = ['TokenRevocationEndpoint']


class TokenRevocationEndpoint(RevocationEndpoint):
    """A Token revocation endpoint."""

    def query_token(self, token: str, token_type_hint: str,
                    client: Client) -> Token:
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

    def revoke_token(self, token: Token):
        """Revokes the respective token."""
        token.revoked = True
        token.save()
