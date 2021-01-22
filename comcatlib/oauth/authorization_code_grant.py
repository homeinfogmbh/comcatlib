"""Authorization code grants."""

from typing import Any, Optional

from authlib.oauth2.rfc6749 import grants

from comcatlib.orm.oauth import AuthorizationCode, Client
from comcatlib.orm.user import User


__all__ = ['AuthorizationCodeGrant']


class AuthorizationCodeGrant(grants.AuthorizationCodeGrant):
    """Handles authorization code grants."""

    TOKEN_ENDPOINT_AUTH_METHODS = ['client_secret_post']

    def save_authorization_code(self, code: str, request: Any) -> None:
        """Saves an authorization code."""
        authorization_code = AuthorizationCode(
            code=code,
            client_id=request.client.client_id,
            redirect_uri=request.redirect_uri,
            scope=request.scope,
            user_id=request.user.id
        )
        authorization_code.save()

    def query_authorization_code(self, code: str, client: Client) \
            -> Optional[AuthorizationCode]:
        """Returns the authorization code."""
        condition = AuthorizationCode.code == code
        condition &= AuthorizationCode.client_id == client.client_id

        try:
            return AuthorizationCode.select(cascade=True).where(
                condition).get()
        except AuthorizationCode.DoesNotExist:
            return None

    def delete_authorization_code(
            self, authorization_code: AuthorizationCode) -> None:
        """Deletes the respective authorization code."""
        authorization_code.delete_instance()

    def authenticate_user(
            self, authorization_code: AuthorizationCode) -> Optional[User]:
        """Authenticates a user."""
        if authorization_code.is_expired():
            return None

        return authorization_code.user
