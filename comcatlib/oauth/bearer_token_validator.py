"""Validation of bearer tokens."""

from typing import Any, Optional

from authlib.oauth2 import rfc6750

from comcatlib.orm import Token


__all__ = ['BearerTokenValidator']


class BearerTokenValidator(rfc6750.BearerTokenValidator):
    """Validates bearer tokens."""

    def authenticate_token(self, token_string: str) -> Optional[Token]:
        """Authenticates a token."""
        try:
            return Token.select(cascade=True).where(
                Token.access_token == token_string).get()
        except Token.DoesNotExist:
            return None

    def request_invalid(self, request: Any) -> bool:
        """Determines whether the request is invalid."""
        return False

    def token_revoked(self, token: Token) -> bool:
        """Determines whether the token is revoked."""
        return token.revoked
