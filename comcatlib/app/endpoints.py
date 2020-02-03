"""Flask based OAuth endpoints."""

from flask import request, render_template, Flask

from comcatlib.app.application import APPLICATION
from comcatlib.app.contextlocals import USER
from comcatlib.app.oauth import SERVER


__all__ = ['APPLICATION']


APPLICATION = Flask('comcat')


@APPLICATION.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    """Login is required since we need to know the current resource owner.
    It can be done with a redirection to the login page, or a login
    form on this authorization page.
    """

    if request.method == 'GET':
        grant = SERVER.validate_consent_request(end_user=USER.instance)
        return render_template(
            'authorize.html', grant=grant, user=USER.instance)

    confirmed = request.form['confirm']

    if confirmed:
        # granted by resource owner
        return SERVER.create_authorization_response(grant_user=USER)

    # denied by resource owner
    return SERVER.create_authorization_response(grant_user=None)


@APPLICATION.route('/oauth/token', methods=['POST'])
def issue_token():
    """Issues a token."""

    return SERVER.create_token_response()
