"""Toaken revication endpoint."""

from authlib.oauth2.rfc7009 import RevocationEndpoint


__all__ = ['TokenRevocationEndpoint']


class TokenRevocationEndpoint(RevocationEndpoint):
    """A Token revocation endpoint."""

    def query_token(self, token, token_type_hint, client):
        """Queries a token from the database."""
        select = client_id=client.client_id

        if token_type_hint == 'access_token':
            select &= Token.access_token == token
        elif token_type_hint == 'refresh_token':
            select &= Token.refresh_token == token
        else:   # without token_type_hint
            select &= Token.refresh_token == token

        try:
            return Token.get(select)
        except Token.DoesNotExist:
            return Token.get(refresh_token=token)

    def revoke_token(self, token):
        """Revokes the respective token."""
        token.revoked = True
        token.save()
