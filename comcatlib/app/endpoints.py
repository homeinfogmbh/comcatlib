"""Flask based OAuth endpoints."""

from comcatlib.app.functions import authorize_client
from comcatlib.app.functions import generate_initialization_nonce
from comcatlib.app.functions import introspect_token
from comcatlib.app.functions import register_client
from comcatlib.app.functions import revoke_token
from comcatlib.oauth import SERVER


__all__ = ['init_oauth_endpoints']


def init_oauth_endpoints(application):
    """Adds OAuth endpoints to the respective application."""

    application.route('/client', methods=['POST'])(register_client)
    application.route('/authorize', methods=['POST'])(authorize_client)
    application.route('/initnonce', methods=['GET'])(
        generate_initialization_nonce)
    application.route('/oauth/token', methods=['POST'])(
        SERVER.create_token_response)
    application.route('/oauth/revoke', methods=['POST'])(revoke_token)
    application.route('/oauth/introspect', methods=['POST'])(introspect_token)
