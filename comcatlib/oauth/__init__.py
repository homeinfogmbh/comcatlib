"""HOMEINFO authentication library using OAuth 2.0."""

from authlib.integrations.flask_oauth2 import ResourceProtector

from comcatlib.oauth.authorization_server import SERVER, init_oauth
from comcatlib.oauth.bearer_token_validator import BearerTokenValidator


__all__ = ['REQUIRE_OAUTH', 'SERVER', 'init_oauth', 'BearerTokenValidator']


REQUIRE_OAUTH = ResourceProtector()
REQUIRE_OAUTH.register_token_validator(BearerTokenValidator())
