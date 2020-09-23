"""Authentication checks."""

from authlib.integrations.flask_oauth2 import current_token, ResourceProtector

from comcatlib.exceptions import UserExpired, UserLocked
from comcatlib.oauth import BearerTokenValidator


__all__ = ['oauth']


RESOURCE_PROTECTOR = ResourceProtector()
RESOURCE_PROTECTOR.register_token_validator(BearerTokenValidator())


def oauth(*args, **kwargs):
    """Performs authentication checks."""

    RESOURCE_PROTECTOR(*args, **kwargs)

    if current_token.user.expired:
        raise UserExpired()

    if current_token.user.locked:
        raise UserLocked()
