"""Web API messages."""

from wsgilib import JSONMessage


__all__ = [
    'NO_SUCH_USER',
    'NO_SUCH_CUSTOMER',
    'SESSION_EXPIRED',
    'USER_LOCKED',
    'USER_ADDED',
    'USER_DELETED',
    'USER_PATCHED',
    'INVALID_CREDENTIALS',
    'NO_ADDRESS_CONFIGURED',
    'ADDRESS_ADDED',
    'ADDRESS_DELETED',
    'INVALID_ADDRESS_VALUE',
    'NO_SUCH_ADDRESS',
    'TENEMENT_ADDED',
    'TENEMENT_DELETED',
    'NO_SUCH_TENEMENT',
    'TENEMENT_PATCHED',
    'INVALID_TENEMENT_VALUE',
    'NO_SUCH_FILE',
    'NOT_LOGGED_IN'
]


NO_SUCH_USER = JSONMessage('The requested user does not exists.', status=404)
NO_SUCH_CUSTOMER = JSONMessage(
    'The requested customer does not exists.', status=404)
SESSION_EXPIRED = JSONMessage('Session expired.', status=401)
USER_LOCKED = JSONMessage('This user is locked.', status=401)
USER_ADDED = JSONMessage('The user has been added.', status=201)
USER_DELETED = JSONMessage('The user has been deleted.', status=200)
USER_PATCHED = JSONMessage('The user has been modified.', status=200)
INVALID_CREDENTIALS = JSONMessage(
    'User name and/or password incorrect.', status=400)
NO_ADDRESS_CONFIGURED = JSONMessage(
    'Account has no address configured.', status=400)
NEWS_NOT_ENABLED = JSONMessage('Module "news" is not enabled.', status=403)
NO_SUCH_ARTICLE = JSONMessage(
    'The requested articles does not exists.', status=404)
NO_SUCH_ARTICLE_IMAGE = JSONMessage(
    'The requested article image does not exists.', status=404)
ADDRESS_ADDED = JSONMessage('The address has been added.', status=201)
ADDRESS_DELETED = JSONMessage('The address has been deleted.', status=200)
INVALID_ADDRESS_VALUE = JSONMessage('Invalid value for address.', status=400)
NO_SUCH_ADDRESS = JSONMessage(
    'The requested address does not eixst.', status=404)
TENEMENT_ADDED = JSONMessage('The tenement has been added.', status=201)
TENEMENT_DELETED = JSONMessage('The tenement has been deleted.', status=200)
NO_SUCH_TENEMENT = JSONMessage(
    'The requested tenement does not eixst.', status=404)
TENEMENT_PATCHED = JSONMessage(
    'The requested tenement has been patched.', status=404)
INVALID_TENEMENT_VALUE = JSONMessage('Invalid value for tenement.', status=400)
NO_SUCH_FILE = JSONMessage('No such file.', status=404)
NOT_LOGGED_IN = JSONMessage('You are not logged-in.', status=401)
