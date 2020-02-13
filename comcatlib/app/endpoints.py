"""Flask based OAuth endpoints."""

from flask import request
from jinja2 import FileSystemLoader, Environment

from comcatlib.app.contextlocals import USER
from comcatlib.oauth import SERVER
from comcatlib.oauth.introspection_endpoint import TokenIntrospectionEndpoint
from comcatlib.oauth.revocation_endpoint import TokenRevocationEndpoint


__all__ = ['init_oauth_endpoints']


TEMPLATE_LOADER = FileSystemLoader(searchpath='/usr/local/share/comcatlib/')
TEMPLATE_ENV = Environment(loader=TEMPLATE_LOADER)
TEMPLATE = TEMPLATE_ENV.get_template('authorize.html')


def authorize():
    """Login is required since we need to know the current resource owner.
    It can be done with a redirection to the login page, or a login
    form on this authorization page.
    """

    if request.method == 'GET':
        grant = SERVER.validate_consent_request(end_user=USER.instance)
        return TEMPLATE.render(grant=grant, user=USER.instance)

    confirmed = request.form['confirm']

    if confirmed:
        # granted by resource owner
        return SERVER.create_authorization_response(grant_user=USER)

    # denied by resource owner
    return SERVER.create_authorization_response(grant_user=None)


def issue_token():
    """Issues a token."""

    return SERVER.create_token_response()


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

    application.route('/oauth/authorize', methods=['GET', 'POST'])(authorize)
    application.route('/oauth/token', methods=['POST'])(issue_token)
    application.route('/oauth/revoke', methods=['POST'])(revoke_token)
    application.route('/oauth/introspect', methods=['POST'])(introspect_token)
