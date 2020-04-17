"""User login."""

from uuid import UUID

from flask import redirect, request, session

from comcatlib.exceptions import InvalidCredentials, UserLocked
from comcatlib.messages import INVALID_CREDENTIALS, NO_SUCH_USER, USER_LOCKED
from comcatlib.orm.user import User
from comcatlib.templates import render_template


__all__ = ['get_current_user', 'login_user', 'login']


def get_current_user():
    """Returns the logged-in user."""

    uid = session.get('uid')

    if not uid:
        return None

    try:
        return User.get(User.id == uid)
    except User.DoesNotExist:
        return None


def login_user():
    """Logs in a user with POSTed form data."""

    uuid = request.form.get('uuid')

    if not uuid:
        raise NO_SUCH_USER

    try:
        uuid = UUID(uuid)
    except ValueError:
        raise NO_SUCH_USER

    passwd = request.form.get('passwd')

    if not passwd:
        raise NO_SUCH_USER

    try:
        user = User.get(User.uuid == uuid)
    except User.DoesNotExist:
        raise INVALID_CREDENTIALS

    try:
        success = user.login(passwd)
    except InvalidCredentials:
        raise INVALID_CREDENTIALS
    except UserLocked:
        raise USER_LOCKED

    if success:
        session['uid'] = user.id

    return user


def login():
    """Renders the home screen."""

    if request.method == 'POST':
        if login_user():
            return redirect('/oauth/authorize')

        return INVALID_CREDENTIALS

    return render_template('login.html')
