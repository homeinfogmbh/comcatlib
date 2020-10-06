"""Handling of refresh tokens."""

from authlib.oauth2.rfc6749 import grants

from comcatlib.orm.oauth import Token
from comcatlib.orm.user import User


__all__ = ['RefreshTokenGrant']


class RefreshTokenGrant(grants.RefreshTokenGrant):
    """Handles refresh token grants."""

    TOKEN_ENDPOINT_AUTH_METHODS = ['client_secret_post']
    INCLUDE_NEW_REFRESH_TOKEN = True

    def authenticate_refresh_token(self, refresh_token):
        """Authenticates the refresh token."""
        try:
            refresh_token = Token.get(refresh_token=refresh_token)
        except Token.DoesNotExist:
            return None

        if refresh_token.revoked:
            return None

        return refresh_token

    def authenticate_user(self, credential):
        """Authenticates the user."""
        try:
            return User[credential.user_id]
        except User.DoesNotExist:
            return None

    def revoke_old_credential(self, credential):
        """Revokes the credential."""
        credential.revoked = True
        credential.save()
