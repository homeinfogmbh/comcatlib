"""User login."""

from uuid import UUID

from flask import redirect, render_template, request, session

from comcatlib.exceptions import InvalidCredentials, UserLocked
from comcatlib.messages import INVALID_CREDENTIALS, NO_SUCH_USER, USER_LOCKED
from comcatlib.orm.oauth import Client
from comcatlib.orm.user import User


__all__ = ['get_current_user', 'login']


def get_current_user():
    """Returns the logged-in user."""

    uid = session.get('uid')

    if not uid:
        return None

    try:
        return User.get(User.id == uid)
    except User.DoesNotExist:
        return None


def _do_login():
    """Performs actual login."""

    uuid = request.form.get('uuid')

    if not uuid:
        return NO_SUCH_USER

    try:
        uuid = UUID(uuid)
    except ValueError:
        return NO_SUCH_USER

    passwd = request.form.get('passwd')

    if not passwd:
        return NO_SUCH_USER

    try:
        user = User.get(User.uuid == uuid)
    except User.DoesNotExist:
        return INVALID_CREDENTIALS

    try:
        success = user.login(passwd)
    except InvalidCredentials:
        return INVALID_CREDENTIALS
    except UserLocked:
        return USER_LOCKED

    if success:
        session['uid'] = user.id
        return redirect('/oauth/authorize')

    return INVALID_CREDENTIALS


def login():
    """Renders the home screen."""

    if request.method == 'POST':
        return _do_login()

    user = get_current_user()

    if user:
        clients = Client.select().where(Client.user == user)
    else:
        clients = []

    return render_template('login.html', user=user, clients=clients)
