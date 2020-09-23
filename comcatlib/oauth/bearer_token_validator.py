"""Validation of bearer tokens."""

from authlib.oauth2 import rfc6750

from comcatlib.orm import Token


__all__ = ['BearerTokenValidator']


class BearerTokenValidator(rfc6750.BearerTokenValidator):
    """Validates bearer tokens."""

    def authenticate_token(self, token_string):
        """Authenticates a token."""
        try:
            return Token.get(Token.access_token == token_string)
        except Token.DoesNotExist:
            return None

    def request_invalid(self, request):
        """Determines whether the request is invalid."""
        return False

    def token_revoked(self, token):
        """Determines whether the token is revoked."""
        return token.revoked
