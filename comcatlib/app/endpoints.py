"""Flask based OAuth endpoints."""

from flask import request, render_template

from comcatlib.oauth import SERVER
from comcatlib.app.contextlocals import USER


__all__ = ['init_oauth_endpoints']


AUTH_TEMPLATE = '/usr/local/share/comcatlib/authorize.html'


def authorize():
    """Login is required since we need to know the current resource owner.
    It can be done with a redirection to the login page, or a login
    form on this authorization page.
    """

    if request.method == 'GET':
        grant = SERVER.validate_consent_request(end_user=USER.instance)
        return render_template(AUTH_TEMPLATE, grant=grant, user=USER.instance)

    confirmed = request.form['confirm']

    if confirmed:
        # granted by resource owner
        return SERVER.create_authorization_response(grant_user=USER)

    # denied by resource owner
    return SERVER.create_authorization_response(grant_user=None)


def issue_token():
    """Issues a token."""

    return SERVER.create_token_response()


def init_oauth_endpoints(application):
    """Adds OAuth endpoints to the respective application."""

    application.route('/oauth/authorize', methods=['GET', 'POST'])(authorize)
    application.route('/oauth/token', methods=['POST'])(issue_token)
