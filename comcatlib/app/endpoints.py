"""Flask based OAuth endpoints."""

from flask import request

from comcatlib.app.clientreg import register_client
from comcatlib.app.login import get_current_user, login
from comcatlib.oauth import SERVER
from comcatlib.oauth.introspection_endpoint import TokenIntrospectionEndpoint
from comcatlib.oauth.revocation_endpoint import TokenRevocationEndpoint
from comcatlib.templates import render_template


__all__ = ['init_oauth_endpoints']


def authorize():
    """Login is required since we need to know the current resource owner.
    It can be done with a redirection to the login page, or a login
    form on this authorization page.
    """

    end_user = get_current_user()

    if not end_user:
        return login(redirect_to_authorize=True)

    if request.method == 'GET':
        grant = SERVER.validate_consent_request(end_user=end_user)
        return render_template('authorize.html', grant=grant, user=end_user)

    confirmed = request.form['confirm']

    if confirmed:
        # granted by resource owner
        return SERVER.create_authorization_response(grant_user=end_user)

    # denied by resource owner
    return SERVER.create_authorization_response(grant_user=None)


def revoke_token():
    """Revokes a token."""

    return SERVER.create_endpoint_response(
        TokenRevocationEndpoint.ENDPOINT_NAME)


def introspect_token():
    """Introspects a token."""

    return SERVER.create_endpoint_response(
        TokenIntrospectionEndpoint.ENDPOINT_NAME)


def init_oauth_endpoints(application):
    """Adds OAuth endpoints to the respective application."""

    application.route('/client', methods=['POST'])(register_client)
    application.route('/login', methods=['GET', 'POST'])(login)
    application.route('/oauth/authorize', methods=['GET', 'POST'])(authorize)
    application.route('/oauth/token', methods=['POST'])(
        SERVER.create_token_response)
    application.route('/oauth/revoke', methods=['POST'])(revoke_token)
    application.route('/oauth/introspect', methods=['POST'])(introspect_token)
