"""Flask based OAuth endpoints."""

from flask import request, render_template

from comcatlib.app.application import APPLICATION
from comcatlib.app.auth import USER
from comcatlib.app.oauth import SERVER


@APPLICATION.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    """Login is required since we need to know the current resource owner.
    It can be done with a redirection to the login page, or a login
    form on this authorization page."""

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
