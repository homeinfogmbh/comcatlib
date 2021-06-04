"""Handling of refresh tokens."""

from typing import Optional

from authlib.oauth2.rfc6749 import grants

from comcatlib.orm.oauth import Token
from comcatlib.orm.user import User


__all__ = ['RefreshTokenGrant']


class RefreshTokenGrant(grants.RefreshTokenGrant):
    """Handles refresh token grants."""

    CLIENT_AUTH_METHODS = ['client_secret_post']
    INCLUDE_NEW_REFRESH_TOKEN = True

    def authenticate_refresh_token(self, refresh_token: str) \
            -> Optional[Token]:
        """Authenticates the refresh token."""
        try:
            refresh_token = Token.select(cascade=True).where(
                Token.refresh_token == refresh_token).get()
        except Token.DoesNotExist:
            return None

        if refresh_token.revoked:
            return None

        return refresh_token

    def authenticate_user(self, credential: Token) -> Optional[User]:
        """Authenticates the user."""
        if credential.is_valid():
            return credential.user

        return None

    def revoke_old_credential(self, credential: Token) -> None:
        """Revokes the credential."""
        credential.revoked = True
        credential.save()
